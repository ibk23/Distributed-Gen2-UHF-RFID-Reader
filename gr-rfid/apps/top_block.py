#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Feb 21 17:24:40 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import rfid
import sys
import time


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 0
        self.rx_gain = rx_gain = 20
        self.num_taps = num_taps = [1] * 25
        self.freq = freq = 910e6
        self.decim = decim = 5
        self.dac_rate = dac_rate = 5e6
        self.ampl = ampl = 0.1
        self.adc_rate = adc_rate = 5e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.2", "recv_frame_size=256")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(adc_rate)
        self.uhd_usrp_source_0.set_center_freq(910000000, 0)
        self.uhd_usrp_source_0.set_gain(15, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("addr=192.168.10.2", "recv_frame_size=256")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(dac_rate)
        self.uhd_usrp_sink_0.set_center_freq(910000000, 0)
        self.uhd_usrp_sink_0.set_gain(15, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.rfid_tag_decoder_0 = rfid.tag_decoder(int(adc_rate/decim))
        self.rfid_reader_0 = rfid.reader(int(adc_rate/decim), int(dac_rate))
        self.rfid_gate_0 = rfid.gate(int(adc_rate / decim))
        self.low_pass_filter_0 = filter.fir_filter_ccf(decim, firdes.low_pass(
        	1, adc_rate, 50000, 10000, firdes.WIN_HAMMING, 6.76))
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(10, ([1]))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(decim, (num_taps))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/cna22/Desktop/Testdata/decoder_carl_test", False)
        self.blocks_file_sink_2.set_unbuffered(False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/cna22/git/Distributed-Gen2-UHF-RFID-Reader/gr-rfid/misc/data/source", False)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/cna22/git/Distributed-Gen2-UHF-RFID-Reader/gr-rfid/misc/data/filter", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, "/home/cna22/git/Distributed-Gen2-UHF-RFID-Reader/gr-rfid/misc/data/reader", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0_1_0 = analog.sig_source_c(dac_rate, analog.GR_COS_WAVE, 2000000, 1, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(dac_rate, analog.GR_COS_WAVE, 2000000, 3, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.analog_sig_source_x_0_1_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_file_sink_2, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.rfid_gate_0, 0))    
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_float_to_complex_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.fir_filter_xxx_0, 0))    
        self.connect((self.rfid_gate_0, 0), (self.rfid_tag_decoder_0, 0))    
        self.connect((self.rfid_reader_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.rfid_reader_0, 0), (self.interp_fir_filter_xxx_0, 0))    
        self.connect((self.rfid_tag_decoder_0, 1), (self.blocks_null_sink_0, 0))    
        self.connect((self.rfid_tag_decoder_0, 0), (self.rfid_reader_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0_0_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_xx_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_num_taps(self):
        return self.num_taps

    def set_num_taps(self, num_taps):
        self.num_taps = num_taps
        self.fir_filter_xxx_0.set_taps((self.num_taps))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_dac_rate(self):
        return self.dac_rate

    def set_dac_rate(self, dac_rate):
        self.dac_rate = dac_rate
        self.analog_sig_source_x_0_1.set_sampling_freq(self.dac_rate)
        self.analog_sig_source_x_0_1_0.set_sampling_freq(self.dac_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.dac_rate)

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl

    def get_adc_rate(self):
        return self.adc_rate

    def set_adc_rate(self, adc_rate):
        self.adc_rate = adc_rate
        self.uhd_usrp_source_0.set_samp_rate(self.adc_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.adc_rate, 50000, 10000, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
