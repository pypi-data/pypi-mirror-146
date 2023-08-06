import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  ContextConnector,
  ICompletionManager,
  KernelConnector
} from '@jupyterlab/completer';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import { CompletionConnector } from '../connectors/connector';

import { CustomConnector } from '../connectors/customConnector';

/**
 * The command IDs used by the console plugin.
 */
namespace CommandIDs {
  export const invoke = 'completer:invoke';

  export const invokeNotebook = 'completer:invoke-notebook-1';

  export const select = 'completer:select';

  export const selectNotebook = 'completer:select-notebook-custom';
}
const SETTINGS_PLUGIN_ID = 'jupyterlab_mutableai:settings-mutableai';

/**
 * Initialization data for the extension.
 */
const completer: JupyterFrontEndPlugin<void> = {
  id: 'completer',
  autoStart: true,
  requires: [ICompletionManager, INotebookTracker, ISettingRegistry],
  activate: async (
    app: JupyterFrontEnd,
    completionManager: ICompletionManager,
    notebooks: INotebookTracker,
    settings: ISettingRegistry
  ) => {
    console.log('Mutable AI custom completer extension is activated!');

    Promise.all([app.restored, settings.load(SETTINGS_PLUGIN_ID)]).then(
      ([, setting]) => {
        // Modelled after completer-extension's notebooks plugin
        const enabled = setting.get('enabled').composite as boolean;
        if (enabled) {
          notebooks.widgetAdded.connect(
            (sender: INotebookTracker, panel: NotebookPanel) => {
              let editor = panel.content.activeCell?.editor ?? null;
              const session = panel.sessionContext.session;
              const options = { session, editor };
              const connector = new CompletionConnector([]);
              const handler = completionManager.register({
                connector,
                editor,
                parent: panel
              });

              const updateConnector = () => {
                editor = panel.content.activeCell?.editor ?? null;
                options.session = panel.sessionContext.session;
                options.editor = editor;
                handler.editor = editor;

                const kernel = new KernelConnector(options);
                const context = new ContextConnector(options);

                /*
                 * The custom connector is getting initialized with settings.
                 * This is used to get the updated settings while making the
                 * completer api call.
                 */
                const custom = new CustomConnector(options, panel, setting);

                handler.connector = new CompletionConnector([
                  custom,
                  kernel,
                  context
                ]);
              };

              // Update the handler whenever the prompt or session changes
              panel.content.activeCellChanged.connect(updateConnector);
              panel.sessionContext.sessionChanged.connect(updateConnector);
            }
          );
          // Add notebook completer command.
          app.commands.addCommand(CommandIDs.invokeNotebook, {
            execute: () => {
              const panel = notebooks.currentWidget;
              if (panel && panel.content.activeCell?.model.type === 'code') {
                return app.commands.execute(CommandIDs.invoke, {
                  id: panel.id
                });
              }
            }
          });

          // Add notebook completer select command.
          app.commands.addCommand(CommandIDs.selectNotebook, {
            execute: () => {
              const id = notebooks.currentWidget && notebooks.currentWidget.id;

              if (id) {
                return app.commands.execute(CommandIDs.select, { id });
              }
            }
          });

          // Set enter key for notebook completer select command.
          app.commands.addKeyBinding({
            command: CommandIDs.selectNotebook,
            keys: ['Enter'],
            selector: '.jp-Notebook .jp-mod-completer-active'
          });
        }
      }
    );
  }
};

export default completer;
