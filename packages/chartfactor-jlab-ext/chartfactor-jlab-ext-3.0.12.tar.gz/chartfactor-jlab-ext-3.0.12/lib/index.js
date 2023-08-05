const RunnerExtension = require('./runner').default;

module.exports = [
  {
    id: 'chartfactor_jlab_ext',
    autoStart: true,
    activate: function (app) {
      // console.log(
      //   'JupyterLab extension chartfactor_jlab_ext is activated!'
      // );
      // console.log(app.commands);
      const runner = new RunnerExtension();
      app.docRegistry.addWidgetExtension('Notebook', runner);
    }
  }
];
