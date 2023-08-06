import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { fastForwardIcon } from '@jupyterlab/ui-components';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { settingsIcon } from '@jupyterlab/ui-components';
import { SettingsWidget } from '../widgets/Settings';
import { IMainMenu, MainMenu } from '@jupyterlab/mainmenu';
import { ITranslator } from '@jupyterlab/translation';

import { requestAPI } from '../handler';

const COMMAND_ID = 'jupyterlab_mutableai/settings:toggle-flag';
const COMMAND_SETTINGS_ID = 'jupyterlab_mutableai/settings:update-settings';

/**
 * Initialization data for the jupyterlab_mutableai extension.
 */

const SETTINGS_PLUGIN_ID = 'jupyterlab_mutableai:settings-mutableai';

// class MenuRenderer extends Menu.Renderer {
//   renderItem(data: Menu.IRenderData): VirtualElement {
//     // data = {
//     //   ...data,
//     //   item: {
//     //     ...data.item,
//     //     label: 'MutableAI Settings'
//     //   }
//     // };
//     console.log('this is called..', data);

//     let className = this.createItemClass(data);
//     let dataset = this.createItemDataset(data);
//     let aria = this.createItemARIA(data);
//     return h.li(
//       {
//         className,
//         dataset,
//         tabindex: '0',
//         onfocus: data.onfocus,
//         ...aria
//       },
//       this.renderIcon(data),
//       this.renderLabel(data),
//       this.renderShortcut(data),
//       this.renderSubmenu(data)
//     );
//   }
// }

const contextMenu: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_mutableai:contextMenu',
  autoStart: true,
  requires: [IFileBrowserFactory, ISettingRegistry, IMainMenu, ITranslator],
  activate: (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    settings: ISettingRegistry,
    mainMenu: IMainMenu,
    translator: ITranslator
  ) => {
    console.log('Mutable AI context menu is activated!');
    let flag = true;
    const trans = translator.load('jupyterlab');
    /**
     * Load the settings for this extension
     *
     * @param setting Extension settings
     */
    function loadSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      flag = setting.get('flag').composite as boolean;
    }

    const command = 'context_menu:open';

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(SETTINGS_PLUGIN_ID)]).then(
      ([, setting]) => {
        // Read the settings
        loadSetting(setting);

        const enabled = setting.get('enabled').composite as boolean;
        if (enabled) {
          const { commands } = app;

          const mutableAiMainMenu = MainMenu.generateMenu(
            commands,
            {
              id: 'mutable-ai-settings',
              label: 'Mutable AI Settings',
              rank: 80
            },
            trans
          );

          mutableAiMainMenu.addGroup([
            {
              command: COMMAND_ID
            },
            {
              command: COMMAND_SETTINGS_ID
            }
          ]);

          mainMenu.addMenu(mutableAiMainMenu, { rank: 80 });
          // Listen for your plugin setting changes using Signal
          setting.changed.connect(loadSetting);

          commands.addCommand(COMMAND_ID, {
            label: 'AutoComplete',
            isToggled: () => flag,
            execute: () => {
              // Programmatically change a setting
              Promise.all([setting.set('flag', !flag)])
                .then(() => {
                  const newFlag = setting.get('flag').composite as boolean;
                  console.log(
                    `Mutable AI updated flag to '${
                      newFlag ? 'enabled' : 'disabled'
                    }'.`
                  );
                })
                .catch(reason => {
                  console.error(
                    `Something went wrong when changing the settings.\n${reason}`
                  );
                });
            }
          });

          commands.addCommand(COMMAND_SETTINGS_ID, {
            label: 'Update Mutable AI Settings',
            execute: () => {
              const close = () => app.shell.currentWidget?.close();
              const content = new SettingsWidget(setting, close);
              const widget = new MainAreaWidget<SettingsWidget>({ content });
              widget.title.label = 'MutableAI Settings';
              widget.title.icon = settingsIcon;
              app.shell.add(widget, 'main');
            }
          });

          commands.addCommand(command, {
            label: 'Fast Forward to Production with MutableAI',
            caption: 'Mutable AI context menu.',
            icon: fastForwardIcon,
            execute: () => {
              const file = factory.tracker.currentWidget
                ?.selectedItems()
                .next();

              const apiKey = setting.get('apiKey').composite as string;
              const transformDomain = setting.get('transformDomain')
                .composite as string;

              const dataToSend = { name: file?.path, apiKey, transformDomain };

              // POST request
              const reply = requestAPI<any>('TRANSFORM_NB', {
                body: JSON.stringify(dataToSend),
                method: 'POST'
              });

              // Log to console
              reply
                .then(response => console.log('Transformed Successfully!'))
                .catch(e => console.log('Transformation failed!', e));
            }
          });
        }
      }
    );
  }
};

export default contextMenu;
