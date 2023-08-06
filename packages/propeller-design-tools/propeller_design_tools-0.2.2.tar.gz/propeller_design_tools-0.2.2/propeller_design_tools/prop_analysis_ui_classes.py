from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from propeller_design_tools.settings import VALID_OPER_PLOT_PARAMS
from propeller_design_tools.funcs import get_all_propeller_dirs
from propeller_design_tools.propeller import Propeller
try:
    from PyQt5 import QtWidgets, QtCore
    from propeller_design_tools.helper_ui_subclasses import PDT_Label, PDT_GroupBox, PDT_ComboBox, PDT_PushButton
    from propeller_design_tools.helper_ui_classes import SingleAxCanvas, AxesComboBoxWidget, PropellerCreationPanelCanvas
except:
    pass


class PropellerSweepWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        super(PropellerSweepWidget, self).__init__()
        main_lay = QtWidgets.QHBoxLayout()
        self.setLayout(main_lay)

        left_lay = QtWidgets.QVBoxLayout()
        center_lay = QtWidgets.QVBoxLayout()
        # right_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(left_lay)
        main_lay.addLayout(center_lay)
        # main_lay.addLayout(right_lay)

        # left layout
        left_lay.addStretch()
        exist_data_grp = PDT_GroupBox('Existing Data (plot controls)')
        exist_data_grp.setMinimumSize(400, 250)
        exist_data_grp.setLayout(QtWidgets.QVBoxLayout())
        left_lay.addWidget(exist_data_grp)
        left_lay.addStretch()
        add_data_grp = PDT_GroupBox('Add Data Points By Range')
        add_data_grp.setMinimumSize(400, 250)
        add_data_grp.setLayout(QtWidgets.QVBoxLayout())
        left_lay.addWidget(add_data_grp)
        left_lay.addStretch()

        # center layout
        self.select_prop_cb = select_prop_cb = PDT_ComboBox(width=200)
        self.pop_select_prop_cb()
        select_prop_cb.currentTextChanged.connect(self.select_prop_cb_changed)
        center_lay.addStretch()
        center_top_lay = QtWidgets.QHBoxLayout()
        center_top_lay.addStretch()
        center_top_lay.addWidget(PDT_Label('Select Propeller:', font_size=14, bold=True))
        center_top_lay.addWidget(select_prop_cb)
        center_top_lay.addStretch()
        center_lay.addLayout(center_top_lay)

        center_bot_lay = QtWidgets.QHBoxLayout()
        center_bot_lay.addStretch()
        self.wvel_3d_view = wvel_3d_view = gl.GLViewWidget()
        wvel_3d_view.setFixedSize(450, 450)
        center_bot_lay.addWidget(wvel_3d_view)
        center_bot_lay.addStretch()
        center_lay.addLayout(center_bot_lay)
        center_lay.addStretch()

        # right layout
        self.metric_plot_widget = PropellerCreationMetricPlotWidget(main_win=main_win)
        main_lay.addWidget(self.metric_plot_widget)

    def pop_select_prop_cb(self):
        item_txts = ['None'] + get_all_propeller_dirs()
        self.select_prop_cb.addItems(item_txts)

    def select_prop_cb_changed(self):
        if self.select_prop_cb.currentText() == 'None':
            self.wvel_3d_view.clear()
            self.metric_plot_widget.axes.clear()
        else:
            self.plot_prop_wvel()
            self.metric_plot_widget.update_data()

    def plot_prop_wvel(self):
        self.wvel_3d_view.clear()
        prop = self.get_current_prop()
        prop.plot_gl3d_wvel_data(view=self.wvel_3d_view)

    def get_current_prop(self):
        txt = self.select_prop_cb.currentText()
        if txt == 'None':
            return None
        else:
            prop = Propeller(txt)
            return prop


class PropellerCreationMetricPlotWidget(QtWidgets.QWidget):
    def __init__(self, main_win: 'InterfaceMainWindow'):
        self.main_win = main_win
        super(PropellerCreationMetricPlotWidget, self).__init__()
        main_lay = QtWidgets.QVBoxLayout()
        self.setLayout(main_lay)
        self.creation_panel_canvas = None

        axes_cb_lay = QtWidgets.QHBoxLayout()
        main_lay.addLayout(axes_cb_lay)
        # self.plot_opts = ['r/R', 'c/R', 'beta(deg)', 'CL', 'CD', 'RE', 'Mach', 'effi', 'effp', 'GAM', 'Ttot', 'Ptot',
        #                   'VA/V', 'VT/V']
        x_txts = ['x-axis'] + VALID_OPER_PLOT_PARAMS
        y_txts = ['y-axis'] + VALID_OPER_PLOT_PARAMS
        self.axes_cb_widg = AxesComboBoxWidget(x_txts=x_txts, y_txts=y_txts, init_xtxt='rpm',
                                               init_ytxt='Efficiency')
        self.xax_cb = self.axes_cb_widg.xax_cb
        self.yax_cb = self.axes_cb_widg.yax_cb
        self.xax_cb.setFixedWidth(130)
        self.yax_cb.setFixedWidth(130)
        self.xax_cb.currentTextChanged.connect(self.update_data)
        self.yax_cb.currentTextChanged.connect(self.update_data)

        axes_cb_lay.addStretch()
        axes_cb_lay.addWidget(PDT_Label('Plot Metric:', font_size=14, bold=True))
        axes_cb_lay.addWidget(self.axes_cb_widg)
        axes_cb_lay.addStretch()

        lay1 = QtWidgets.QHBoxLayout()
        lay1.addStretch()
        lay1.addWidget(PDT_Label('families of:', font_size=12))
        self.fam_cb = fam_cb = PDT_ComboBox(width=130)
        fam_cb.addItems(['None'] + VALID_OPER_PLOT_PARAMS)
        fam_cb.currentTextChanged.connect(self.update_data)
        lay1.addWidget(fam_cb)
        lay1.addWidget(PDT_Label('iso metric:', font_size=12))
        self.iso_cb = iso_cb = PDT_ComboBox(width=130)
        iso_cb.addItems(['None'] + VALID_OPER_PLOT_PARAMS)
        iso_cb.currentTextChanged.connect(self.update_data)
        lay1.addWidget(iso_cb)
        lay1.addStretch()
        main_lay.addLayout(lay1)

        self.plot_canvas = SingleAxCanvas(self, width=4.5, height=5)
        self.axes = self.plot_canvas.axes
        main_lay.addWidget(self.plot_canvas)
        toolbar = NavigationToolbar(self.plot_canvas, self)
        main_lay.addWidget(toolbar)
        main_lay.setAlignment(toolbar, QtCore.Qt.AlignHCenter)
        main_lay.addStretch()

    def update_data(self):
        self.plot_canvas.clear_axes()

        yax_txt = self.yax_cb.currentText()
        xax_txt = self.xax_cb.currentText()
        if yax_txt == 'y-axis' or xax_txt == 'x-axis':
            return
        prop = self.main_win.prop_sweep_widg.get_current_prop()
        if prop is None:
            return

        fam_txt = self.fam_cb.currentText()
        if fam_txt.lower() == 'none':
            fam_txt = None

        iso_txt = self.iso_cb.currentText()
        if iso_txt.lower() == 'none':
            iso_txt = None

        prop.oper_data.plot(x_param=xax_txt, y_param=yax_txt, family_param=fam_txt, iso_param=iso_txt,
                            fig=self.plot_canvas.figure)

        # self.axes.set_xlabel(xax_txt)
        # self.axes.set_ylabel(yax_txt)
        # self.axes.grid(True)
        # xdata = prop.xrotor_op_dict[xax_txt]
        # if yax_txt in prop.blade_data:
        #     self.axes.plot(xdata, prop.blade_data[yax_txt], marker='*', markersize=4)
        # else:
        #     if yax_txt in prop.xrotor_op_dict:
        #         self.axes.plot(xdata, prop.xrotor_op_dict[yax_txt], marker='o', markersize=3)

        self.plot_canvas.draw()
