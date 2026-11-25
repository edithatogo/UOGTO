"""Build the versioned UOGTO references from the exact upstream releases."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import tarfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/processed/external-games/catalogues.jsonld"
BASE = "https://w3id.org/uogto/catalogues"
GAMBIT = "https://github.com/gambitproject/gambit/blob/v16.7.0"
OPEN_SPIEL = "https://github.com/google-deepmind/open_spiel/blob/v2.0.2"
SOURCES = {
    "gambit": "35a2d7df4f8181cb216ce9a2b10ca820724768d8c69787a608a4a2725a745278",
    "gambit_catalog": "cfa0ffee6879b510e04ff1f8922ab6309f7610995800c4ae2430eb66be7cf6ec",
    "gamut": "3469fafaacf38b6fa2c30fc9d41501fb36f1b37811ca9d40be7964df2f698949",
    "openspiel": "6f520dfe499b9e5e1e3a31cf77bf071abb02b98104789e7698021922a064e856",
}
CONTEXT = {
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "prov": "http://www.w3.org/ns/prov#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "spdx": "http://spdx.org/rdf/terms#",
    "uogto": "https://w3id.org/uogto/core#",
    "uogtox": "https://w3id.org/uogto/extensions#",
    "identifier": "dct:identifier",
    "label": "rdfs:label",
    "alternative": "dct:alternative",
    "format": "dct:format",
    "version": "dcat:version",
    "catalogue": {"@id": "dct:isPartOf", "@type": "@id"},
    "subject": {"@id": "dct:subject", "@type": "@id"},
    "source": {"@id": "prov:wasDerivedFrom", "@type": "@id"},
    "download": {"@id": "dcat:downloadURL", "@type": "@id"},
    "checksum": {"@id": "spdx:checksum", "@type": "@id"},
    "algorithm": {"@id": "spdx:algorithm", "@type": "@id"},
    "checksumValue": "spdx:checksumValue",
}
QUOTED = r'"(?:\\.|[^"\\])*"'
CPP_COMMENT_OR_STRING = re.compile(rf"({QUOTED})|//[^\n]*|/\*[\s\S]*?\*/")
CPP_REGISTRATION = re.compile(r"\bREGISTER_SPIEL_GAME\(\s*(\w+)\s*,")
OPEN_SPIEL_FACTS = re.compile(
    r"GameType::(Dynamics|ChanceMode|Information|Utility|RewardModel)::(\w+)"
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def verify_file(path, key):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != SOURCES[key]:
        raise ValueError(f"{key} source differs from its frozen release")


def read_archive(path):
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            if member.isfile():
                resource = PurePosixPath(member.name)
                relative = PurePosixPath(*resource.parts[1:])
                with archive.extractfile(member) as stream:
                    yield relative, stream.read()


def checksum(digest):
    return {
        "@id": f"urn:sha256:{digest}",
        "@type": "spdx:Checksum",
        "algorithm": "spdx:checksumAlgorithm_sha256",
        "checksumValue": digest,
    }


def record(catalogue, key, label, format_name, source_uri, data, subjects):
    return {
        "@id": f"{catalogue}/{quote(key, safe='/')}",
        "@type": "prov:Entity",
        "catalogue": catalogue,
        "identifier": key,
        "label": label or key,
        "format": format_name,
        "source": {"@id": source_uri, "checksum": checksum(sha256(data))},
        "subject": subjects,
    }


def gambit_models(path):
    for relative, data in read_archive(path):
        if relative.suffix not in {".efg", ".nfg"}:
            continue
        if relative.parts[0] == "catalog":
            parent = f"{BASE}/gambit/16.7.0/models"
            model = PurePosixPath(*relative.parts[1:])
        elif relative.parts[:2] == ("contrib", "games"):
            parent = f"{BASE}/gambit/16.7.0/contributed"
            model = PurePosixPath(*relative.parts[2:])
        else:
            continue
        key = (model.with_suffix("") if relative.parts[0] == "catalog" else model).as_posix()
        text = data.decode("utf-8-sig", errors="replace")
        header = re.match(rf"\s*(?:EFG|NFG)\s+\d+\s+\w+\s+({QUOTED})", text)
        if header is None and relative.parts[0] == "catalog":
            raise ValueError(f"missing Gambit catalogue header: {relative}")
        subject = (
            "uogto:NormalFormRepresentation"
            if model.suffix == ".nfg"
            else "uogto:ExtensiveFormRepresentation"
        )
        yield record(
            parent,
            key,
            ast.literal_eval(header[1]) if header else key,
            model.suffix[1:].upper(),
            f"{GAMBIT}/{quote(relative.as_posix())}",
            data,
            [subject],
        )


def gamut_classes(path, archive):
    source = path.read_bytes()
    definitions = [
        node.value
        for node in ast.parse(source).body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "_GAMUT_GAMES" for target in node.targets
        )
    ]
    (definition,) = definitions
    aliases = {"GuessThirdsAve": "GuessTwoThirdsAve", "ShapleyGame": "ShapleysGame"}
    advertised = {
        aliases.get(entry["Class"], entry["Class"]): entry["Class"]
        for entry in ast.literal_eval(definition)
    }
    (registry,) = [
        data
        for relative, data in read_archive(archive)
        if relative.as_posix() == "edu/stanford/multiagent/gamer/games.txt"
    ]
    entries = dict(
        tuple(part.strip() for part in line.split("=", 1))
        for line in registry.decode("ascii").splitlines()
        if line.strip() and not line.startswith("#")
    )
    if {key for key, body in entries.items() if not body} != set(advertised):
        raise ValueError("Gambit's GAMUT classes differ from the official registry")
    for key, body in entries.items():
        kind = (
            "GAMUT" if not body else "GAMUT preset" if body.startswith("[") else "GAMUT collection"
        )
        row = record(
            f"{BASE}/gambit/16.7.0/gamut",
            key,
            key,
            kind,
            "https://gamut.stanford.edu/gamut.src.tgz#src/edu/stanford/multiagent/gamer/games.txt",
            registry,
            ["uogto:NormalFormRepresentation"],
        )
        if key in advertised and key != advertised[key]:
            row["alternative"] = advertised[key]
        yield row


def cpp_types(source):
    code = CPP_COMMENT_OR_STRING.sub(lambda match: match[1] or " ", source)
    for registration in CPP_REGISTRATION.finditer(code):
        declarations = list(
            re.finditer(
                rf"\bGameType\s+{registration[1]}\s*(?:=\s*)?\{{\s*({QUOTED})\s*,\s*({QUOTED})([\s\S]*?);",
                code[: registration.start()],
            )
        )
        if not declarations:
            raise ValueError(f"unresolved OpenSpiel C++ GameType: {registration[1]}")
        declaration = declarations[-1]
        facts = dict(OPEN_SPIEL_FACTS.findall(declaration[3]))
        yield ast.literal_eval(declaration[1]), ast.literal_eval(declaration[2]), facts


def attribute_path(expr):
    if isinstance(expr, ast.Attribute):
        return (*attribute_path(expr.value), expr.attr)
    if isinstance(expr, ast.Name):
        return (expr.id,)
    return ()


def python_types(source):
    calls = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call)]
    registrations = sum(attribute_path(call.func) == ("pyspiel", "register_game") for call in calls)
    if not registrations:
        return
    game_types = [call for call in calls if attribute_path(call.func) == ("pyspiel", "GameType")]
    if len(game_types) != registrations:
        raise ValueError("OpenSpiel Python GameType and registration counts differ")
    for call in game_types:
        fields = {item.arg: item.value for item in call.keywords}
        facts = {}
        for value in fields.values():
            path = attribute_path(value)
            if path[:2] == ("pyspiel", "GameType") and len(path) == 4:
                facts[path[2]] = path[3]
        yield ast.literal_eval(fields["short_name"]), ast.literal_eval(fields["long_name"]), facts


def subjects(facts):
    dynamics = facts.get("Dynamics", "").removeprefix("k").replace("_", "").lower()
    information = facts.get("Information", "").removeprefix("k").replace("_", "").lower()
    if dynamics == "meanfield":
        return ["uogtox:MeanFieldGame"]
    if dynamics == "sequential":
        return ["uogto:ExtensiveFormRepresentation"]
    if dynamics == "simultaneous" and information == "oneshot":
        return ["uogto:NormalFormRepresentation"]
    if dynamics in {"", "simultaneous"}:
        return ["uogto:GameSpecification"]
    raise ValueError(f"unknown OpenSpiel dynamics {dynamics}")


def openspiel_games(path):
    for relative, data in read_archive(path):
        directory = relative.parts[:2]
        if relative.as_posix() in {
            "open_spiel/python/coalitional_games/wvg.py",
            "open_spiel/python/examples/ppo_example.py",
        }:
            weighted = relative.name == "wvg.py"
            yield record(
                f"{BASE}/openspiel/2.0.2",
                "weighted_voting" if weighted else "atari",
                "Weighted Voting Games" if weighted else "Atari integration",
                "OpenSpiel integration",
                f"{OPEN_SPIEL}/{relative}",
                data,
                ["uogtox:CooperativeGame"] if weighted else ["uogto:GameSpecification"],
            )
            continue
        if (
            relative.suffix == ".cc"
            and not relative.name.endswith("_test.cc")
            and directory
            in (
                ("open_spiel", "games"),
                ("open_spiel", "game_transforms"),
            )
        ):
            entries = cpp_types(data.decode("utf-8"))
            format_name = (
                "OpenSpiel transform" if directory[1] == "game_transforms" else "OpenSpiel C++"
            )
        elif (
            relative.suffix == ".py"
            and directory == ("open_spiel", "python")
            and b"pyspiel.register_game(" in data
        ):
            entries = python_types(data)
            format_name = "OpenSpiel Python"
        else:
            continue
        try:
            for key, label, facts in entries:
                yield record(
                    f"{BASE}/openspiel/2.0.2",
                    key,
                    label,
                    "OpenSpiel loader" if key in {"nfg_game", "efg_game"} else format_name,
                    f"{OPEN_SPIEL}/{quote(relative.as_posix())}",
                    data,
                    subjects(facts),
                )
        except (KeyError, ValueError, SyntaxError) as error:
            raise ValueError(f"{relative}: {error}") from error


def dataset(identifier, label, version, url, digest):
    return {
        "@id": identifier,
        "@type": "dcat:Dataset",
        "label": label,
        "version": version,
        "download": url,
        "checksum": checksum(digest),
    }


def build(gambit, gambit_catalog, gamut, openspiel):
    for path, key in (
        (gambit, "gambit"),
        (gambit_catalog, "gambit_catalog"),
        (gamut, "gamut"),
        (openspiel, "openspiel"),
    ):
        verify_file(path, key)
    releases = [
        dataset(
            f"{BASE}/gambit/16.7.0/models",
            "Gambit packaged model catalogue",
            "16.7.0",
            "https://github.com/gambitproject/gambit/releases/download/v16.7.0/gambit-16.7.0.tar.gz",
            SOURCES["gambit"],
        ),
        dataset(
            f"{BASE}/gambit/16.7.0/contributed",
            "Gambit contributed models and parser fixtures",
            "16.7.0",
            "https://github.com/gambitproject/gambit/releases/download/v16.7.0/gambit-16.7.0.tar.gz",
            SOURCES["gambit"],
        ),
        dataset(
            f"{BASE}/gambit/16.7.0/gamut",
            "GAMUT generator registry linked from Gambit",
            "1.0.1",
            "https://gamut.stanford.edu/gamut.src.tgz",
            SOURCES["gamut"],
        ),
        dataset(
            f"{BASE}/openspiel/2.0.2",
            "OpenSpiel bundled game definitions",
            "2.0.2",
            "https://files.pythonhosted.org/packages/bb/3b/9d56d511eff27e26714aa232c945bb00335f792bc1959637ee0d2639a018/open_spiel-2.0.2.tar.gz",
            SOURCES["openspiel"],
        ),
    ]
    entries = sorted(
        (
            *gambit_models(gambit),
            *gamut_classes(gambit_catalog, gamut),
            *openspiel_games(openspiel),
        ),
        key=lambda item: item["@id"],
    )
    if len({entry["@id"] for entry in entries}) != len(entries):
        raise ValueError("duplicate upstream definition identifiers")
    return {"@context": CONTEXT, "@graph": [*releases, *entries]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gambit", type=Path, required=True)
    parser.add_argument("--gambit-catalog", type=Path, required=True)
    parser.add_argument("--gamut", type=Path, required=True)
    parser.add_argument("--openspiel", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalogue = build(args.gambit, args.gambit_catalog, args.gamut, args.openspiel)
    rendered = (json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes() != rendered:
            raise SystemExit("committed catalogue differs from the frozen upstream releases")
    else:
        OUTPUT.write_bytes(rendered)
    print(f"{sum('identifier' in row for row in catalogue['@graph'])} definition references")


if __name__ == "__main__":
    main()
