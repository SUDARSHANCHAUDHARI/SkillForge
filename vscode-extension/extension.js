
const vscode = require('vscode');
const { execFile } = require('child_process');

function runCommand(args, label) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) {
        vscode.window.showErrorMessage('SkillForge: No workspace folder open.');
        return;
    }

    execFile('python', ['-m', 'cli.main', ...args], { cwd: workspaceRoot }, (err, stdout, stderr) => {
        const output = (stdout || stderr || 'No output.').trim();
        if (err) {
            vscode.window.showErrorMessage(`SkillForge ${label} failed: ${output}`);
        } else {
            vscode.window.showInformationMessage(`SkillForge ${label}: ${output}`);
        }
    });
}

function activate(context) {
    context.subscriptions.push(
        vscode.commands.registerCommand('skillforge.audit', () => {
            runCommand(['audit', './skills'], 'Audit');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('skillforge.duplicates', () => {
            runCommand(['duplicates', './skills'], 'Duplicates');
        })
    );
}

exports.activate = activate;
