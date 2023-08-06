import { IMainMenu, MainMenu } from '@jupyterlab/mainmenu';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { ContextMenuSvg, RankedMenu } from '@jupyterlab/ui-components';
import { PromiseDelegate } from '@lumino/coreutils';
import { IMutableAI } from './tokens';
import { toggleFlag, updateSettings } from './commands';
import { CommandRegistry } from '@lumino/commands';
import { IDisposable } from '@lumino/disposable';

export class MutableAIManager implements IMutableAI {
  constructor(options: IMutableAI.IOptions) {
    this.mutableAiMainMenu = null;
    this._translator = options.translator ?? nullTranslator;
    this._mainMenu = options.mainMenu;
    this._commands = options.commands;
    this._contextMenu = options.contextMenu;
    this._processFilePointer = null;

    options
      .getSettings()
      .then(mutableAI => {
        this._mutableAI = mutableAI;
        this._mutableAI.changed.connect(this._mutableAISettingsChanged, this);
        this._mutableAISettingsChanged();
        this._ready.resolve();
      })
      .catch(reason => {
        console.warn(reason);
        this._ready.reject(reason);
      });
  }

  /*
    Mutable AI manager extension enable port.
  */
  enable() {
    this._mutableAI?.set('enabled', true);
  }

  /*
    Mutable AI manager extension disable port.
  */
  disable() {
    this._mutableAI?.set('enabled', false);
  }

  /*
    Mutable AI manager extension initialization.
  */
  private initializePlugin() {
    this.dispose();
    const enabled = this._mutableAI?.get('enabled').composite as boolean;
    if (enabled) {
      const trans = this._translator.load('jupyterlab');

      this.mutableAiMainMenu = MainMenu.generateMenu(
        this._commands,
        {
          id: 'mutable-ai-settings',
          label: 'Mutable AI Settings',
          rank: 80
        },
        trans
      );

      this.mutableAiMainMenu.addGroup([
        {
          command: toggleFlag
        },
        {
          command: updateSettings
        }
      ]);

      this._mainMenu.addMenu(this.mutableAiMainMenu, { rank: 80 });

      this._processFilePointer = this._contextMenu.addItem({
        command: 'context_menu:open',
        selector: '.jp-DirListing-item[data-file-type="notebook"]',
        rank: 0
      });
    }
  }

  /*
    Mutable AI manager extension dispose.
  */
  private dispose() {
    this.mutableAiMainMenu?.dispose();
    this._processFilePointer?.dispose();
  }

  /**
   * A promise that resolves when the settings have been loaded.
   */
  get ready(): Promise<void> {
    return this._ready.promise;
  }

  /**
   * Mutable AI manager change extension according to settings.
   */
  private _mutableAISettingsChanged(): void {
    const enabled = this._mutableAI?.get('enabled').composite as boolean;
    if (enabled) {
      this.initializePlugin();
    } else {
      this.dispose();
    }
  }

  mutableAiMainMenu: RankedMenu | null;
  private _contextMenu: ContextMenuSvg;
  private _processFilePointer: IDisposable | null;
  private _commands: CommandRegistry;
  private _ready = new PromiseDelegate<void>();
  private _translator: ITranslator;
  private _mainMenu: IMainMenu;
  private _mutableAI: ISettingRegistry.ISettings | null = null;
}
