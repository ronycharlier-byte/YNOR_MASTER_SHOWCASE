# MIROIR TEXTUEL - GPT_ACTION_SCHEMA.yaml

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\GPT_ACTION_SCHEMA.yaml
Taille : 2586 octets
SHA256 : e619e6c82db90087839494d0f290cd9981b8ede0982f97fe0e69273089ed20b9

```text
openapi: 3.1.0
info:
  title: MDL Ynor - MILLENNIUM EDITION
  description: Moteur Quantique AGI d'évaluation mathématique et de dissipation.
  version: 3.4.0
servers:
  - url: https://gastrointestinal-interprovincial-vania.ngrok-free.dev
    description: Serveur Ynor (Ngrok Live Tunnel)
paths:
  /v1/agent/hierarchical_query:
    post:
      operationId: computeYnorMu
      summary: Audit d'un Vecteurs de Données Stochastiques AGI (Équation Mu)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query: {type: string}
                alpha_capacity: {type: number}
                beta_pressure: {type: number}
                kappa_memory: {type: number}
              required: [query, alpha_capacity, beta_pressure, kappa_memory]
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: {type: string}
                  agent_response: {type: string}
  /status:
    get:
      operationId: getSystemStatus
      summary: Vérifier le statut du système
      responses:
        "200":
          description: OK
  /v1/mu/history:
    get:
      operationId: getMuHistory
      summary: Historique des Audits Mu (Analyse de tendance)
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    timestamp: {type: number}
                    mu: {type: number}
  /v1/archive/auto_learn:
    post:
      operationId: archiveExperience
      summary: Archiver une Expérience Client
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                session_id: {type: string}
                experience_summary: {type: string}
                quality_score: {type: number}
              required: [session_id, experience_summary, quality_score]
      responses:
        "200":
          description: OK
  /privacy:
    get:
      operationId: getPrivacyPolicy
      summary: Politique de Confidentialité Ynor
      responses:
        "200":
          description: OK
components:
  schemas: {}
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-Ynor-API-Key
security:
  - ApiKeyAuth: []

```