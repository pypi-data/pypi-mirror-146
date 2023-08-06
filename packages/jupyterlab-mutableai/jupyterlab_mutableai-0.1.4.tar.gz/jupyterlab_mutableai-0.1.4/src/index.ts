import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import contextMenu from './plugins/contextMenu';
import settings from './plugins/settings';
import completer from './plugins/completer';

/**
 * Initialization data for the jupyterlab_mutableai extension.
 */
const plugins: JupyterFrontEndPlugin<any>[] = [
  contextMenu,
  settings,
  completer
];

export default plugins;
