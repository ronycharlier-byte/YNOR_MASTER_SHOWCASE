param(
    [ValidateSet("P0", "P1", "P2", "All")]
    [string]$Priority = "All",

    [int]$Limit = 0,

    [ValidateSet("auto", "latexmk", "pdflatex", "xelatex", "lualatex")]
    [string]$Compiler = "auto"
)

$ErrorActionPreference = "Stop"

function Get-CompilerCommand {
    param([string]$Preferred)

    $miktexBin = [IO.Path]::Combine($env:LOCALAPPDATA, "Programs", "MiKTeX", "miktex", "bin", "x64")
    $miktexCandidates = @(
        [IO.Path]::Combine($miktexBin, "latexmk.exe"),
        [IO.Path]::Combine($miktexBin, "pdflatex.exe"),
        [IO.Path]::Combine($miktexBin, "xelatex.exe"),
        [IO.Path]::Combine($miktexBin, "lualatex.exe")
    )

    if ($Preferred -ne "auto") {
        $cmd = Get-Command $Preferred -ErrorAction SilentlyContinue
        if ($null -eq $cmd) {
            foreach ($candidatePath in $miktexCandidates) {
                if ([IO.Path]::GetFileNameWithoutExtension($candidatePath) -eq $Preferred -and (Test-Path -LiteralPath $candidatePath)) {
                    return $candidatePath
                }
            }
            throw "Le compilateur '$Preferred' est introuvable dans le PATH."
        }
        return $cmd.Name
    }

    foreach ($candidate in @("latexmk", "pdflatex", "xelatex", "lualatex")) {
        $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($null -ne $cmd) {
            return $cmd.Name
        }
    }

    foreach ($candidatePath in $miktexCandidates) {
        if (Test-Path -LiteralPath $candidatePath) {
            return $candidatePath
        }
    }

    throw "Aucun compilateur LaTeX n'est disponible (latexmk/pdflatex/xelatex/lualatex)."
}

function Invoke-LatexBuild {
    param(
        [string]$Source,
        [string]$CompilerName
    )

    $sourcePath = Resolve-Path -LiteralPath $Source
    $workDir = Split-Path -Parent $sourcePath.Path
    $fileName = Split-Path -Leaf $sourcePath.Path

    Push-Location $workDir
    try {
        $compilerLeaf = [IO.Path]::GetFileNameWithoutExtension($CompilerName)
        if ($compilerLeaf -eq "latexmk") {
            & $CompilerName -pdf -interaction=nonstopmode -halt-on-error -file-line-error $fileName
        } else {
            & $CompilerName -interaction=nonstopmode -halt-on-error -file-line-error $fileName
            & $CompilerName -interaction=nonstopmode -halt-on-error -file-line-error $fileName
        }
    } finally {
        Pop-Location
    }
}

$constitutionRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$jobs = @(
    @{ Priority = "P0"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\M2.tex" },
    @{ Priority = "P0"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\MDL_Ynor_Dynamic_Systems_Paper.tex" },
    @{ Priority = "P0"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\MDL_YNOR_POST_MILLENNIUM_REPORT_PHASE_I_II.tex" },
    @{ Priority = "P0"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\MDL_YNOR_POST_MILLENNIUM_REPORT_PHASE_III.tex" },
    @{ Priority = "P0"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III\Sovereign_Unification_Phase_III_Manuscrit.tex" },
    @{ Priority = "P0"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\Sovereign_Unification_Phase_III_Manuscrit.tex" },

    @{ Priority = "P1"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\MDL_YNOR_MILLENNIUM_DISSIPATIVE_STABILITY.tex" },
    @{ Priority = "P1"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\MDL_Ynor_NeurIPS_Submission.tex" },
    @{ Priority = "P1"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III\PHASE_IV_ACCESS_CARD.tex" },
    @{ Priority = "P1"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\PHASE_IV_ACCESS_CARD.tex" },
    @{ Priority = "P1"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III\Sovereign_Millennium_Dissipative_Stability_Proof.tex" },
    @{ Priority = "P1"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\Sovereign_Millennium_Dissipative_Stability_Proof.tex" },

    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_01_THEORY_AND_PAPERS\MDL_YNOR_NAVIER_STOKES_PROFESSOR_AUDIT.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\MDL_GPT_KNOWLEDGE_PRODUCTION\MDL_YNOR_POST_MILLENNIUM_REPORT_PHASE_I_II.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\MDL_GPT_KNOWLEDGE_PRODUCTION\MDL_YNOR_POST_MILLENNIUM_REPORT_PHASE_III.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\MDL_GPT_KNOWLEDGE_PRODUCTION\MDL_YNOR_MILLENNIUM_DISSIPATIVE_STABILITY.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES\MDL_Ynor_Dynamic_Systems_Paper.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "MDL_Ynor_Framework\_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES\MDL_Ynor_NeurIPS_Submission.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\Numerical_Verification_Report_Phases_I_II.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III\PHASE_IV_ACCESS_CARD.fractale_augmente.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III\Sovereign_Millennium_Dissipative_Stability_Proof.fractale_augmente.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III\Sovereign_Unification_Phase_III_Manuscrit.fractale_augmente.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\Numerical_Verification_Report_Phases_I_II.fractale_augmente.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\PHASE_IV_ACCESS_CARD.fractale_augmente.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\Sovereign_Millennium_Dissipative_Stability_Proof.fractale_augmente.tex" },
    @{ Priority = "P2"; Source = Join-Path $constitutionRoot "..\..\07_A_PRIME_ARCHIVES_ET_RELEASES\08_PDF_LATEX_CHIASTIQUES_AUGMENTES\_RELEASES\GOLDEN_MASTER_PHASE_III_SOUVERAINE\Sovereign_Unification_Phase_III_Manuscrit.fractale_augmente.tex" }
)

if ($Priority -ne "All") {
    $jobs = $jobs | Where-Object { $_.Priority -eq $Priority }
}

if ($Limit -gt 0) {
    $jobs = $jobs | Select-Object -First $Limit
}

$compilerName = Get-CompilerCommand -Preferred $Compiler
Write-Host "Compilateur utilise: $compilerName"
Write-Host "Travaux a executer: $($jobs.Count)"

$results = @()
foreach ($job in $jobs) {
    $source = $job.Source
    if (-not (Test-Path -LiteralPath $source)) {
        $results += [pscustomobject]@{
            Priority = $job.Priority
            Source   = $source
            Status   = "Missing"
            Message  = "Source introuvable"
        }
        continue
    }

    try {
        Invoke-LatexBuild -Source $source -CompilerName $compilerName
        $results += [pscustomobject]@{
            Priority = $job.Priority
            Source   = $source
            Status   = "OK"
            Message  = "PDF reconstruit"
        }
    } catch {
        $results += [pscustomobject]@{
            Priority = $job.Priority
            Source   = $source
            Status   = "Failed"
            Message  = $_.Exception.Message
        }
    }
}

$results | Format-Table -AutoSize
$failed = $results | Where-Object { $_.Status -eq "Failed" }
if ($failed.Count -gt 0) {
    exit 1
}
