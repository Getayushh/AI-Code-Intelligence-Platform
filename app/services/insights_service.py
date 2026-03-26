def generate_insights(data):
    """
    Generate summary insights from clone + cluster data
    """

    total_files = data.get("total_files", 0)

    type1 = len(data.get("type1_clones", []))
    type2 = len(data.get("type2_clones", []))
    type3 = len(data.get("type3_clones", []))
    type4 = len(data.get("type4_clones", []))

    clusters = data.get("clusters", [])

    # 🔹 Duplication score
    total_clones = type1 + type2 + type3 + type4

    if total_files == 0:
        duplication_ratio = 0
    else:
        duplication_ratio = total_clones / total_files

    # 🔹 Risk level
    if duplication_ratio < 0.5:
        risk = "Low"
    elif duplication_ratio < 1.5:
        risk = "Medium"
    else:
        risk = "High"

    # 🔹 Generate insights
    insights = []

    if type1 > 0:
        insights.append(f"{type1} exact duplicate files detected")

    if type2 > 0:
        insights.append(f"{type2} token-level similarities found")

    if type3 > 0:
        insights.append(f"{type3} structural similarities detected")

    if type4 > 0:
        insights.append(f"{type4} semantic similarities detected")

    if len(clusters) > 0:
        insights.append(f"{len(clusters)} clusters of similar files identified")

    # 🔹 Suggestions
    suggestions = []

    if type1 > 0:
        suggestions.append("Remove duplicate code and reuse modules")

    if type2 > 0 or type3 > 0:
        suggestions.append("Refactor similar logic into reusable functions")

    if type4 > 0:
        suggestions.append("Review semantically similar implementations for optimization")

    if len(clusters) > 2:
        suggestions.append("Consider modularizing clustered components")

    # 🔹 Final summary
    summary = f"{risk} duplication risk with {total_clones} clone relationships detected"

    return {
        "summary": summary,
        "risk_level": risk,
        "duplication_ratio": round(duplication_ratio, 2),
        "insights": insights,
        "suggestions": suggestions
    }