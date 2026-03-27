// Show selected filename
document.getElementById("fileInput").addEventListener("change", function () {
    const label = document.getElementById("file-name-label");
    label.textContent = this.files[0] ? this.files[0].name : "No file selected";
});

async function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        showError("Please select a ZIP file first.");
        return;
    }

    if (!file.name.endsWith(".zip")) {
        showError("Only .zip files are supported.");
        return;
    }

    // Reset UI
    hideError();
    document.getElementById("loading").style.display = "flex";
    document.getElementById("dashboard").style.display = "none";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:8000"
        : "https://YOUR_HF_USERNAME-ai-code-intelligence.hf.space";

const response = await fetch(`${API_BASE}/analyze`, {
            method: "POST",
            body: formData
        });

        // ✅ FIX: Check HTTP status before parsing JSON
        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log("API RESPONSE:", data);

        renderDashboard(data);

    } catch (error) {
        // ✅ FIX: Show error in UI instead of just alert()
        showError("❌ " + (error.message || "Unknown error. Is the backend running?"));
    } finally {
        document.getElementById("loading").style.display = "none";
    }
}


function renderDashboard(data) {

    document.getElementById("dashboard").style.display = "block";

    // ✅ FIX: Guard against missing fields
    const insights = data.insights || {};
    const insightsList = Array.isArray(insights.insights) ? insights.insights : [];
    const suggestionsList = Array.isArray(insights.suggestions) ? insights.suggestions : [];

    // 🔹 Summary
    document.getElementById("summary").innerHTML = `
        <div class="card summary-card">
            <div class="stat"><span class="stat-label">Total Files</span><span class="stat-value">${data.total_files ?? 0}</span></div>
            <div class="stat"><span class="stat-label">Risk Level</span><span class="stat-value">${insights.risk_level ?? "N/A"}</span></div>
            <div class="stat"><span class="stat-label">Duplication Ratio</span><span class="stat-value">${insights.duplication_ratio ?? "0.00"}</span></div>
        </div>
    `;

    // 🔹 Clone Detection
    const t1 = data.type1_clones?.length ?? 0;
    const t2 = data.type2_clones?.length ?? 0;
    const t3 = data.type3_clones?.length ?? 0;
    const t4 = data.type4_clones?.length ?? 0;

    document.getElementById("clones").innerHTML = `
        <div class="card clone-card">
            <div class="clone-stat ${t1 > 0 ? "has-clones" : ""}">
                <span>🔴 Type 1 (Exact Match)</span>
                <span class="clone-count">${t1} pair(s)</span>
            </div>
            <div class="clone-stat ${t2 > 0 ? "has-clones" : ""}">
                <span>🟠 Type 2 (Token-Based)</span>
                <span class="clone-count">${t2} pair(s)</span>
            </div>
            <div class="clone-stat ${t3 > 0 ? "has-clones" : ""}">
                <span>🟡 Type 3 (AST-Based)</span>
                <span class="clone-count">${t3} pair(s)</span>
            </div>
            <div class="clone-stat ${t4 > 0 ? "has-clones" : ""}">
                <span>🔵 Type 4 (Semantic)</span>
                <span class="clone-count">${t4} pair(s)</span>
            </div>
        </div>
    `;

    // 🔹 Clusters
    const clusters = Array.isArray(data.clusters) ? data.clusters : [];
    if (clusters.length === 0) {
        document.getElementById("clusters").innerHTML = `<div class="card muted">No clusters found — files are sufficiently distinct.</div>`;
    } else {
        let clusterHTML = "";
        clusters.forEach(cluster => {
            clusterHTML += `
                <div class="card">
                    <strong>Cluster ${cluster.cluster_id}</strong> — ${cluster.size} file(s)<br>
                    <ul class="file-list">
                        ${cluster.files.map(f => `<li>${f}</li>`).join("")}
                    </ul>
                </div>
            `;
        });
        document.getElementById("clusters").innerHTML = clusterHTML;
    }

    // 🔹 Insights
    let insightsHTML = `<div class="card">`;
    insightsHTML += `<p class="summary-text">${insights.summary ?? ""}</p>`;

    if (insightsList.length > 0) {
        insightsHTML += `<ul class="insight-list">`;
        insightsList.forEach(i => { insightsHTML += `<li>💬 ${i}</li>`; });
        insightsHTML += `</ul>`;
    }

    if (suggestionsList.length > 0) {
        insightsHTML += `<h3>✅ Suggestions</h3><ul class="insight-list suggestions">`;
        suggestionsList.forEach(s => { insightsHTML += `<li>→ ${s}</li>`; });
        insightsHTML += `</ul>`;
    }

    insightsHTML += `</div>`;
    document.getElementById("insights").innerHTML = insightsHTML;
}


// ── Helpers ──────────────────────────────────────────────────────────────────

function showError(message) {
    const box = document.getElementById("error-box");
    box.textContent = message;
    box.style.display = "block";
}

function hideError() {
    const box = document.getElementById("error-box");
    box.style.display = "none";
    box.textContent = "";
}
