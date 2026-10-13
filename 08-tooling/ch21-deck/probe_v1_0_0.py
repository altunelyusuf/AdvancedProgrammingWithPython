import json, io, os, sys, tempfile, warnings
warnings.simplefilter('ignore')
R = {}
def t(f):
    try: return f()
    except BaseException as e: return type(e).__name__
def run():
    import importlib.metadata as m
    R['Python'] = sys.version.split()[0]
    R['Pillow'] = t(lambda: m.version('pillow'))
    R['Matplotlib'] = t(lambda: m.version('matplotlib'))
    from PIL import Image, ImageDraw, ImageFont, ImageColor
    d = tempfile.mkdtemp(); os.chdir(d); Image.new('RGB', (3, 3)).save('z.png')
    R['filename is absolute'] = str(os.path.isabs(Image.open('z.png').filename))
    R['ImageDraw.textsize'] = str(hasattr(ImageDraw.ImageDraw, 'textsize'))
    R['default font'] = type(ImageFont.load_default()).__name__
    R['green'] = str(ImageColor.getcolor('green', 'RGBA'))
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    R['pie returns'] = t(lambda: type(plt.pie([1, 2, 3])).__name__)
    R['line colour is'] = t(lambda: type(plt.plot([1, 2])[0].get_color()).__name__)
    plt.close('all')
    R['savefig'] = t(lambda: (plt.plot([1, 2]), plt.savefig(io.BytesIO(), format='png'), 'saved')[2])
    plt.close('all')
    R['legend'] = t(lambda: (plt.plot([1, 2], label='a'), type(plt.legend()).__name__)[1])
try: run()
except BaseException as e: R['import'] = type(e).__name__
print(json.dumps(R))
