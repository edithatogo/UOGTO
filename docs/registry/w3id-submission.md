# w3id Namespace Redirect Submission

## Status
Not yet submitted. The `https://w3id.org/uogto/core#` and `https://w3id.org/uogto/extensions#` namespace IRIs are documented in the ontology, but the corresponding w3id redirects are not live yet.

## Requested w3id Repository Change
- Repository: <https://github.com/perma-id/w3id.org>
- Requested path: `uogto/.htaccess`
- Documentation target: <https://edithatogo.github.io/UOGTO/>
- Canonical RDF release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl>

Hash fragments are not sent to HTTP servers, so `https://w3id.org/uogto/core#` is resolved by configuring the `/uogto/core` path, and `https://w3id.org/uogto/extensions#` is resolved by configuring the `/uogto/extensions` path.

## Proposed `.htaccess`
```apache
RewriteEngine On
RewriteRule ^$ https://edithatogo.github.io/UOGTO/ [R=303,L]
RewriteRule ^core/?$ https://edithatogo.github.io/UOGTO/ [R=303,L]
RewriteRule ^extensions/?$ https://edithatogo.github.io/UOGTO/ [R=303,L]
```

## Submission Checklist
- [x] Confirm current strict registry live check fails on missing w3id redirects.
- [x] Prepare the proposed `uogto/.htaccess` redirect rules.
- [x] Generate machine-readable handoff packet with `make w3id-packet`.
- [ ] Submit pull request to `perma-id/w3id.org`.
- [ ] Record w3id pull request URL.
- [ ] Verify `https://w3id.org/uogto/core#` returns a live redirect after merge.
- [ ] Verify `https://w3id.org/uogto/extensions#` returns a live redirect after merge.
- [ ] Remove pending w3id blocker from registry checklist after live verification.

## Submission Record
- Pull request URL: `TBD`
- Review status: `Not submitted`
- Merge status: `TBD`
