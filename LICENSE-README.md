# License Information

## Open Source Components

The AEGIS Bloom toolkit (`aegis-bloom` Python package) is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.

This includes:
- Bloom filter implementation
- Python bindings
- CLI tools for `bloom-build` and `bloom-check`
- Example scripts and documentation

## Enterprise Components

The following components are **NOT** included in this open-source release and are available under separate commercial licensing:

- **AEGIS Prover**: Zero-Knowledge proof generation for model weights
- **Nova ZK-SNARK implementation**: Cryptographic binding of weights to datasets
- **Cloud attestation services**: Notarized proofs with legal standing
- **Enterprise dashboard**: Multi-tenant compliance management
- **KZG commitments**: Advanced cryptographic primitives
- **HSM integration**: Hardware security module support

For access to enterprise features, please contact:
- Email: enterprise@aegisprove.com
- Web: https://aegisprove.com/enterprise

## Community vs Enterprise

| Feature | Community (MIT) | Enterprise (EULA) |
|---------|-----------------|-------------------|
| Bloom filters | ✅ Unlimited | ✅ Unlimited |
| Local copyright checks | ✅ Yes | ✅ Yes |
| False positive rate | 1% | 0.01% configurable |
| Dataset size | Unlimited | Unlimited |
| Cryptographic proofs | ❌ No | ✅ Yes |
| Legal attestation | ❌ No | ✅ Yes |
| Cloud notarization | ❌ No | ✅ Yes |
| Support | Community | 24/7 SLA |
| Indemnification | ❌ No | ✅ Available |

## Patents and Trademarks

"AEGIS" is a trademark of AEGIS Testing Technologies, Inc.

Certain cryptographic techniques used in the enterprise version may be covered by pending patent applications. The open-source bloom filter implementation uses only standard, unencumbered algorithms.

## Questions?

For licensing questions, please open an issue or contact legal@aegisprove.com.
