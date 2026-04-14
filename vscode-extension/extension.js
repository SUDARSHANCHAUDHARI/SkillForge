
const vscode = require('vscode');
const { execFile } = require('child_process');

const outputChannel = vscode.window.createOutputChannel('SkillForge');

function runCommand(args, label) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) {
        vscode.window.showErrorMessage('SkillForge: No workspace folder open.');
        return;
    }

    outputChannel.show(true);
    outputChannel.appendLine(`\n▶ SkillForge ${label}  (${new Date().toLocaleTimeString()})`);
    outputChannel.appendLine('─'.repeat(50));

    execFile('python', ['-m', 'cli.main', ...args], { cwd: workspaceRoot }, (err, stdout, stderr) => {
        const output = (stdout || stderr || 'No output.').trim();
        outputChannel.appendLine(output);
        if (err) {
            vscode.window.showErrorMessage(`SkillForge ${label} failed. See Output panel.`);
        } else {
            vscode.window.showInformationMessage(`SkillForge ${label} complete. See Output panel.`);
        }
    });
}

function activate(context) {
    context.subscriptions.push(
        vscode.commands.registerCommand('skillforge.audit', () => {
            runCommand(['audit', './skills', '--verbose'], 'Audit');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('skillforge.duplicates', () => {
            runCommand(['duplicates', './skills'], 'Duplicates');
        })
    );
}

exports.activate = activate;
