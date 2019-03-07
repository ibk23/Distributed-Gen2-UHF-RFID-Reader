#Developed by: Nikos Kargas 
import sys
print(sys.argv)

from gnuradio import gr
from gnuradio import uhd
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import analog
from gnuradio import digital
from gnuradio import qtgui
import rfid
import time


from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-f1", "--freq1", dest="freq1", required=True,
                    help="USRP1 frequency", metavar="float",type=float)
parser.add_argument("-f2", "--freq2", dest="freq2", required=True,
                    help="USRP2 frequency", metavar="float",type=float)
parser.add_argument("-p1", "--pow1", dest="pow1", required=True,
                    help="USRP1 power", metavar="float",type=float)
parser.add_argument("-p2", "--pow2", dest="pow2", required=True,
                    help="USRP2 power", metavar="float",type=float)

parser.add_argument("-single_tx", action="store_true", dest="single_tx", 
                    help="Only transmit on single USRP (192.168.10.2)")
parser.add_argument("-fd", "--fake_data", dest="fake_data",default=False,
                    help="Transmit Fake data 0.5 for 0.5M DAC, 1 or 2.",type=str)
parser.add_argument("-cw", "--cont_wave",action="store_true", dest="cont_wave",
                    help="Transmit CW signal on tx2.")
parser.add_argument("-d", "--delay", dest="delay_n",default=False,
                    help="Delay tx2 by n samples.", type = int)

args = parser.parse_args()
print(args)

if args.delay_n:
  if (args.cont_wave):
    print("Not allowed both delay and CW. CW takes priority.")
  if args.single_tx:
    print("Not allowed both delay and single_tx. Disabling delay")
    args.delay_n=False
  if args.freq1 != args.freq2:
    print('*'*32)
    print("WARNING - delaying transmission but freq1 and freq2 are not equal")
    print("freq1=%3.2f freq2=%3.2f"%(args.freq1,args.freq2))
    print('*'*32)
if (not args.cont_wave and args.delay_n):
  print("Delaying one transmitter by %i samples"%args.delay_n)


class reader_top_block(gr.top_block):

  # Configure usrp source
  def u_source(self):
    self.source = uhd.usrp_source(
    device_addr=self.usrp_address_source,
    stream_args=uhd.stream_args(
    cpu_format="fc32",
    channels=range(1),
    ),
    )
    self.source.set_samp_rate(self.adc_rate)
    self.source.set_center_freq(self.tx_freq_1, 0)
    self.source.set_gain(self.rx_gain, 0)
    self.source.set_antenna("RX2", 0)
    self.source.set_auto_dc_offset(False) # Uncomment this line for SBX daughterboard

  # Configure usrp sink
  def u_sink(self):
    if args.single_tx:
      self.sink = uhd.usrp_sink(
      device_addr=self.usrp_address_sink,
      stream_args=uhd.stream_args(
      cpu_format="fc32",
      channels=range(1),
      ),
      )
      self.sink.set_samp_rate(self.dac_rate)
      self.sink.set_center_freq(self.tx_freq_1, 0)
      self.sink.set_gain(self.tx_gain_1, 0)
      self.sink.set_antenna("TX/RX", 0)

    else:
      self.sink = uhd.usrp_sink(
      device_addr=self.usrp_address_sink,
      stream_args=uhd.stream_args(
      cpu_format="fc32",
      channels=range(2),
      ),
      )
      self.sink.set_clock_source("mimo", 1)
      self.sink.set_time_source("mimo", 1)
      self.sink.set_samp_rate(self.dac_rate)
      #self.sink.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
      #self.sink.set_time_unknown_pps(uhd.time_spec())
      self.sink.set_center_freq(self.tx_freq_1, 0)
      self.sink.set_gain(self.tx_gain_1, 0)
      self.sink.set_antenna("TX/RX", 0)
      self.sink.set_center_freq(self.tx_freq_2, 1)
      self.sink.set_gain(self.tx_gain_2, 1)
      self.sink.set_antenna("TX/RX", 1)
    
  def __init__(self):
    gr.top_block.__init__(self)

    rt = gr.enable_realtime_scheduling() 

    ######## Variables #########
    self.dac_rate = 2e6 # DAC rate 
    self.adc_rate = 2e6 # ADC rate (2MS/s complex samples)
    self.decim     = 5  # Decimation (downsampling factor)
    self.ampl     = 0.5 # Output signal amplitude (signal power vary for different RFX900 cards)
    # Modulation frequency (can be set between 902-920)
    self.tx_freq_1 = args.freq1*1e6
    # Modulation frequency (can be set between 902-920)
    self.tx_freq_2 = args.freq2*1e6  
    self.rx_gain   = 20   # RX Gain (gain at receiver)
    self.tx_gain_1   = args.pow1  # RFX900 no Tx gain option
    self.tx_gain_2   = args.pow2  # RFX900 no Tx gain option
    
    if args.single_tx:
      self.usrp_address_source = "addr=192.168.10.2,recv_frame_size=256"
      self.usrp_address_sink   = "addr=192.168.10.2,recv_frame_size=256"
    else:
      self.usrp_address_source = "addr0=192.168.10.2, addr1=192.168.20.2,recv_frame_size=256"
      self.usrp_address_sink   = "addr0=192.168.10.2, addr1=192.168.20.2,recv_frame_size=256"

    # Each FM0 symbol consists of ADC_RATE/BLF samples (2e6/40e3 = 50 samples)
    # 10 samples per symbol after matched filtering and decimation
    self.num_taps     = [1] * 2*int(self.adc_rate/(2*2*40e3*self.decim)) # matched to half symbol period
	# Take half, round then double to ensure even number.
    print("Half symbol length is ",2*int(self.adc_rate/(2*2*40e3*self.decim)))
    ######## File sinks for debugging (1 for each block) #########
    self.file_sink_source         = blocks.file_sink(gr.sizeof_gr_complex*1, 
                                    "../misc/data/source", False)
    self.file_sink_matched_filter = blocks.file_sink(gr.sizeof_gr_complex*1,   
                                    "../misc/data/matched_filter", False)
    self.file_sink_gate           = blocks.file_sink(gr.sizeof_gr_complex*1,  
                                    "../misc/data/gate", False)
    self.file_sink_decoder        = blocks.file_sink(gr.sizeof_gr_complex*1,  
                                    "../misc/data/decoder", False)
    self.file_sink_reader         = blocks.file_sink(gr.sizeof_float*1,       
                                    "../misc/data/reader", False)
    self.file_sink_sink           = blocks.file_sink(gr.sizeof_gr_complex*1,  
                                    "../misc/data/sink", False)
    if args.delay_n:
      self.delay = blocks.delay(gr.sizeof_gr_complex*1, args.delay_n)

    ######## Blocks #########
    #self.low_pass  = filter.fir_filter_ccc(self.decim, self.num_taps);
    self.low_pass = filter.fir_filter_ccf(self.decim, firdes.low_pass(
        	1, self.adc_rate, 200000, 100000, firdes.WIN_HAMMING, 6.76))
    #self.low_pass = filter.fir_filter_ccf(5, firdes.low_pass(1, self.adc_rate, 50000, 50000, firdes.WIN_HAMMING, 6.76))
    self.gate = rfid.gate(int(self.adc_rate/self.decim))
    self.tag_decoder = rfid.tag_decoder(int(self.adc_rate/self.decim))
    if args.fake_data=='0.5':
      self.reader = blocks.file_source(gr.sizeof_float*1, 
                            "../misc/data/file_reader_test_0.5M",False)
    elif args.fake_data=='1':
      self.reader = blocks.file_source(gr.sizeof_float*1, 
                            "../misc/data/file_reader_test_1M",False)
    elif args.fake_data=='2':
      self.reader = blocks.file_source(gr.sizeof_float*1,
                            "../misc/data/file_reader_test_2M",False)
    elif args.fake_data==False:
      self.reader = rfid.reader(int(self.adc_rate/self.decim),int(self.dac_rate))
    else:
      print("Fake data parameter not specified correctly. Transmitting real data.")
      self.reader = rfid.reader(int(self.adc_rate/self.decim),int(self.dac_rate))

    self.amp             = blocks.multiply_const_ff(self.ampl)
    self.to_complex      = blocks.float_to_complex()
    self.null_sink = blocks.null_sink(gr.sizeof_float*1)


    if args.cont_wave:
      self.const_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, .4)
    
    elif args.delay_n:
      self.delay = blocks.delay(gr.sizeof_gr_complex*1, args.delay_n)

    # Removed option for DEBUG. Not needed and convolutes the code.
    # USRP blocks
    self.u_source()
    self.u_sink()

    ######## Connections #########
    self.connect(self.source,  self.low_pass)
    self.connect(self.low_pass, self.gate)

    self.connect(self.gate, self.tag_decoder)

    if args.fake_data:
      self.connect((self.tag_decoder,0),self.null_sink) #No longer need this data
    else:
      self.connect((self.tag_decoder,0), self.reader)
    self.connect(self.reader, self.amp)
    self.connect(self.amp, self.to_complex)
    self.connect(self.to_complex, (self.sink,0))

    if args.cont_wave:
      self.connect(self.const_1, (self.sink,1))
    elif args.delay_n:
      self.connect(self.to_complex, self.delay)
      self.connect(self.delay, (self.sink,1))
    elif args.single_tx:
        pass
    else:
      self.connect(self.to_complex, (self.sink,1))

    
    #File sinks for logging (Remove comments to log data)
    #self.connect(self.source, self.file_sink_source)


    
    #File sinks for logging 
    self.connect(self.source,self.file_sink_source)
    self.connect(self.gate, self.file_sink_gate)
    self.connect((self.tag_decoder,1), self.file_sink_decoder) # (Do not comment this line)
    self.connect(self.reader, self.file_sink_reader)
    self.connect(self.low_pass, self.file_sink_matched_filter)
    self.connect((self.to_complex),self.file_sink_sink)

if __name__ == '__main__':
  if not (900<args.freq1<931 and 900<args.freq2<931 and args.pow1<14.1 and args.pow2<14.1):
    print("Looks like freq or power is wrong, quitting.",args)
    sys.exit()

  main_block = reader_top_block()
  main_block.start()
  time.sleep(3)
  #while(1):
  #  inp = raw_input("'Q' to quit \n")
  #  if (inp == "q" or inp == "Q"):
  #    break
  if not args.fake_data:
    main_block.reader.print_results()
  main_block.stop()
