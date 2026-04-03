# MIROIR TEXTUEL - mdl_ynor_portal.html

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\mdl_ynor_portal.html
Taille : 3525 octets
SHA256 : d64687a0722450b3d1e4ce16517ad5c1f8c3c3c441a1a8081b64ed80f15a5ee2

```text
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MDL YNOR | ABYSS ALPHA</title>
    <style>
        :root { --p: #00e5ff; --bg: #050505; --t: #ffffff; }
        * { box-sizing: border-box; }
        body { 
            background: var(--bg); 
            color: var(--t); 
            font-family: 'Inter', system-ui, -apple-system, sans-serif; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
            overflow: hidden;
            background-image: radial-gradient(circle at center, rgba(0, 229, 255, 0.05) 0%, transparent 70%);
        }
        .m-card { 
            background: rgba(255, 255, 255, 0.01); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            padding: 4rem; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 0 100px rgba(0, 229, 255, 0.03);
            backdrop-filter: blur(10px);
            max-width: 600px;
            width: 90%;
            transition: 1s ease;
        }
        .m-card:hover { border-color: rgba(0, 229, 255, 0.2); box-shadow: 0 0 150px rgba(0, 229, 255, 0.05); }
        h1 { 
            font-size: 4rem; 
            margin: 0; 
            color: var(--p); 
            letter-spacing: -4px; 
            filter: drop-shadow(0 0 20px rgba(0, 229, 255, 0.2));
            font-weight: 800;
        }
        p { 
            opacity: 0.4; 
            font-size: 0.9rem; 
            letter-spacing: 5px; 
            text-transform: uppercase; 
            margin-top: 10px;
        }
        .status-bar {
            margin-top: 3rem;
            font-size: 0.7rem;
            color: var(--p);
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.6;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        .dot { width: 6px; height: 6px; background: var(--p); border-radius: 50%; box-shadow: 0 0 10px var(--p); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        .b-btn { 
            background: none; 
            border: 1px solid rgba(0, 229, 255, 0.2); 
            padding: 1rem 3rem; 
            border-radius: 2px; 
            color: var(--p); 
            font-weight: 200; 
            cursor: pointer; 
            margin-top: 3.5rem; 
            transition: 0.5s;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .b-btn:hover { background: var(--p); color: #000; box-shadow: 0 0 40px var(--p); border-color: var(--p); }
        .footer {
            position: absolute;
            bottom: 30px;
            font-size: 0.6rem;
            opacity: 0.2;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="m-card">
        <h1>MDL YNOR</h1>
        <p>Principal Investigatorure AGI Canonique</p>
        
        <div class="status-bar">
            <div class="dot"></div>
            NOYAU : ACTIF | MARGE MU : STABLE
        </div>

        <button class="b-btn" onclick="window.location.href='/pricing'">Initialiser la Connexion</button>
    </div>

    <div class="footer">
        Gouvernance : Principal Investigatore Suprême | Empire MDL Ynor &copy; 2026
    </div>
</body>
</html>

```