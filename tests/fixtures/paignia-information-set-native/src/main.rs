//! Consume the RDF projection with the pinned native Paignia builder.

use std::collections::BTreeMap;
use std::io;

use paignia_core::{
    build_information_set_graph, ActionEdge, ActionId, ChanceEdge, Game, GameSpecification,
    InformationSetDeclaration, InformationSetDefinition, InformationSetError, InformationSetId,
    Node, NodeId, PlayerId,
};
use serde::Deserialize;
use serde_json::json;

const PROVIDER_REVISION: &str = "d4047c0648a89f2aee4461ff70bbc9641e5320cd";
const SPECIFICATION: &str = "https://example.org/doors#specification";
const REPRESENTATION: &str = "https://example.org/doors#extensive";
const PLAYER: &str = "https://example.org/doors#décideur";
const ROOT: &str = "https://example.org/doors#deal";
const LEFT: &str = "https://example.org/doors/left#choice";
const RIGHT: &str = "https://example.org/doors/right#choice";
const PLAY: &str = "https://example.org/doors#play";
const PASS: &str = "https://example.org/doors#pass";

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Projection {
    specification_iri: String,
    representation_iri: String,
    root_iri: String,
    state_types: BTreeMap<String, String>,
    provider_revision: String,
    declaration: Declaration,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Declaration {
    schema_version: String,
    semantic_profile: String,
    sets: Vec<Set>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Set {
    id: String,
    player: String,
    members: Vec<String>,
}

impl From<Declaration> for InformationSetDeclaration {
    fn from(source: Declaration) -> Self {
        Self {
            schema_version: source.schema_version,
            semantic_profile: source.semantic_profile,
            sets: source
                .sets
                .into_iter()
                .map(|set| InformationSetDefinition {
                    id: InformationSetId(set.id),
                    player: PlayerId(set.player),
                    members: set.members.into_iter().map(NodeId).collect(),
                })
                .collect(),
        }
    }
}

fn decision(edges: [(&str, &str); 2]) -> Node {
    Node::Decision {
        player: PlayerId(PLAYER.into()),
        edges: edges
            .into_iter()
            .map(|(action, target)| ActionEdge {
                action: ActionId(action.into()),
                target: NodeId(target.into()),
            })
            .collect(),
    }
}

fn terminal(payoff: f64) -> Node {
    Node::Terminal {
        payoffs: BTreeMap::from([(PlayerId(PLAYER.into()), payoff)]),
    }
}

// This finite topology and its ordered actions are specified independently of the RDF projection.
fn source() -> GameSpecification {
    GameSpecification {
        schema_version: "1.0.0".into(),
        id: SPECIFICATION.into(),
        game: Game {
            root: NodeId(ROOT.into()),
            nodes: [
                (
                    ROOT,
                    Node::Chance {
                        edges: [LEFT, RIGHT]
                            .into_iter()
                            .map(|target| ChanceEdge {
                                probability: 0.5,
                                target: NodeId(target.into()),
                            })
                            .collect(),
                    },
                ),
                (LEFT, decision([("play", PLAY), ("pass", PASS)])),
                (RIGHT, decision([("play", PLAY), ("pass", PASS)])),
                (PLAY, terminal(1.0)),
                (PASS, terminal(0.0)),
            ]
            .into_iter()
            .map(|(node, definition)| (NodeId(node.into()), definition))
            .collect(),
        },
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let projection: Projection = serde_json::from_reader(io::stdin().lock())?;
    let source = source();
    assert_eq!(projection.specification_iri, source.id);
    assert_eq!(projection.representation_iri, REPRESENTATION);
    assert_eq!(projection.root_iri, source.game.root.0);
    let state_types = source
        .game
        .nodes
        .iter()
        .map(|(id, node)| {
            let kind = match node {
                Node::Chance { .. } => "ChanceNode",
                Node::Decision { .. } => "DecisionNode",
                Node::Terminal { .. } => "TerminalNode",
            };
            (id.0.clone(), format!("https://w3id.org/uogto/core#{kind}"))
        })
        .collect::<BTreeMap<_, _>>();
    assert_eq!(projection.state_types, state_types);
    assert_eq!(projection.provider_revision, PROVIDER_REVISION);
    let declaration = InformationSetDeclaration::from(projection.declaration);
    let graph = build_information_set_graph(&source, &declaration)?;
    let (set_id, set) = graph.sets.first_key_value().expect("expected a set");
    assert_eq!(graph.sets.len(), 1);

    let mut wrong_player = declaration.clone();
    wrong_player.sets[0].player = PlayerId("https://example.org/doors#foreign-player".into());
    let owner = build_information_set_graph(&source, &wrong_player).unwrap_err();
    assert!(
        matches!(&owner, InformationSetError::PlayerMismatch { actual, .. } if actual.0 == PLAYER)
    );

    let mut incomplete = declaration.clone();
    incomplete.sets[0].members.retain(|id| id.0 != RIGHT);
    let missing_member = build_information_set_graph(&source, &incomplete).unwrap_err();
    assert_eq!(
        missing_member,
        InformationSetError::UnassignedDecisionNode(NodeId(RIGHT.into()))
    );

    let mut reversed = source.clone();
    reversed.game.nodes.insert(
        NodeId(RIGHT.into()),
        decision([("pass", PASS), ("play", PLAY)]),
    );
    let action_order = build_information_set_graph(&reversed, &declaration).unwrap_err();
    assert!(
        matches!(&action_order, InformationSetError::ActionMismatch { node, .. } if node.0 == RIGHT)
    );

    let mut imperfect = source;
    imperfect.game.nodes.insert(
        NodeId(ROOT.into()),
        decision([("choose-left", LEFT), ("choose-right", RIGHT)]),
    );
    let mut with_root = declaration;
    with_root.sets.push(InformationSetDefinition {
        id: InformationSetId("https://example.org/doors#root-set".into()),
        player: PlayerId(PLAYER.into()),
        members: vec![NodeId(ROOT.into())],
    });
    let recall = build_information_set_graph(&imperfect, &with_root).unwrap_err();
    assert!(
        matches!(&recall, InformationSetError::ImperfectRecall { node, .. } if node.0 == RIGHT)
    );

    println!(
        "{}",
        json!({
            "specification_iri": graph.specification_id.0,
            "id": set_id.0,
            "player": set.player.0,
            "members": set.members.iter().map(|member| &member.0).collect::<Vec<_>>(),
            "actions": set.legal_actions.iter().map(|action| &action.0).collect::<Vec<_>>(),
            "assignments": graph.assignments.iter().map(|(node, set)| (&node.0, &set.0))
                .collect::<BTreeMap<_, _>>(),
            "rejections": [owner.code(), missing_member.code(), action_order.code(), recall.code()],
        })
    );
    Ok(())
}
