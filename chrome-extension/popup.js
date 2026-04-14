
function getTimestamp() {
    const d = new Date();
    return d.toISOString().slice(0, 10);
}

function analyzeText(text) {
    const issues = [];
    if (text.trim().length < 50) issues.push('Too short (under 50 chars)');
    if (text.trim().length > 2000) issues.push('Too long (over 2000 chars)');
    if (text.trim().split(/\s+/).length < 5) issues.push('Too vague — fewer than 5 words');
    const lower = text.toLowerCase();
    if (lower.includes('summarize') && !/(bullet|points|list|format|structure)/.test(lower)) {
        issues.push('Vague summarization — no output format specified');
    }
    return issues;
}

document.getElementById('save').onclick = () => {
    const text = prompt('Paste your prompt:');
    if (!text) return;
    const filename = `prompt-${getTimestamp()}.md`;
    const blob = new Blob([text], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    chrome.downloads.download({ url, filename, saveAs: false }, () => {
        URL.revokeObjectURL(url);
    });
};

document.getElementById('analyze').onclick = () => {
    const text = prompt('Paste your prompt to analyze:');
    if (!text) return;
    const issues = analyzeText(text);
    const output = document.getElementById('output');
    if (issues.length === 0) {
        output.style.color = 'green';
        output.textContent = '✔ Clean';
    } else {
        output.style.color = '#c00';
        output.textContent = issues.map(i => '⚠ ' + i).join('\n');
    }
};
