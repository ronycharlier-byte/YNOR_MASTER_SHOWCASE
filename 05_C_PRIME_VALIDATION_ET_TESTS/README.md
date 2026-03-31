# 05 C PRIME VALIDATION ET TESTS

## Role
Branche miroir de validation: stress tests, reproductibilite, audits de partage public, benchmarks et guides CI.

## Ce Que Cette Branche Contient
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/tests/test_mdl_robustness.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/tests/test_shareable_mu_audit.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_08_EXPERIMENTS_AND_DEMOS/hardcore_validation.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_08_EXPERIMENTS_AND_DEMOS/run_experiment.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_08_EXPERIMENTS_AND_DEMOS/mdl_ynor_ultimate_benchmark_v3.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/.github/workflows/mdl_full_check.yml`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/.github/workflows/ynor_ci.yml`

## Fonction
Cette branche sert a verifier que la branche `C`:
- calcule correctement mu
- resiste aux cas limites
- produit des liens publics partageables
- reste reproductible quand les graines sont fixees
- passe les audits de CI

## Documents De Reference
- [TEST_MATRIX.md](./TEST_MATRIX.md)
- [REPRODUCIBILITY_PROTOCOL.md](./REPRODUCIBILITY_PROTOCOL.md)
- [ROBUSTNESS_AUDIT.md](./ROBUSTNESS_AUDIT.md)
- [BENCHMARK_REPORT.md](./BENCHMARK_REPORT.md)
- [BENCHMARK_FRONTIER_MATH.md](./BENCHMARK_FRONTIER_MATH.md)
- [CI_GUIDE.md](./CI_GUIDE.md)

## Ordre De Lecture
1. Les tests unitaires et d integration.
2. Le protocole de reproductibilite.
3. L audit de robustesse.
4. Le benchmark.
5. Les workflows CI.

