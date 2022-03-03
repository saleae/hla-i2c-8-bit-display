# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting


# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'i2c-address': {
            'format': '{{data.description}}'
        },
        'i2c-data': {
            'format': '{{data.description}}'
        }
    }

    def __init__(self):
        pass

    def decode(self, frame: AnalyzerFrame):
        if frame.type == 'address':
            direction = 'Read' if frame.data['read'] else 'Write'
            address = (frame.data['address'][0] << 1) | (1 if frame.data['read'] else 0)
            message = ''
            if 'ack' in frame.data:
                message = 'ACK' if frame.data['ack'] else 'NAK'
            elif 'error' in frame.data:
                message = frame.data['error']
            return AnalyzerFrame('i2c-address', frame.start_time, frame.end_time, {
                'description': 'Setup {} to [0x{:02X}] + {}'.format(direction, address, message)
            })
        elif frame.type == 'data':
            data = frame.data['data'][0]
            message = ''
            if 'ack' in frame.data:
                message = 'ACK' if frame.data['ack'] else 'NAK'
            elif 'error' in frame.data:
                message = frame.data['error']
            return AnalyzerFrame('i2c-data', frame.start_time, frame.end_time, {
                'description': '0x{:02X} + {}'.format(data, message)
            })
