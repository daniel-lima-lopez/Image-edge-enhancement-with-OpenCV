import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

class EdgeEnhancer:
    def __init__(self, path, minVAl=400, maxVAl=450):
        self.img = cv.imread(path)
        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB) # transformacion a RGB
        self.minVAl = minVAl
        self.maxVAl = maxVAl
    
    def enhance(self):
        self.edges = cv.Canny(self.img, self.minVAl, self.maxVAl)
        
        # transformamos a int32 para operar sin overflow o underflow
        aux_img = np.array(self.img, dtype=np.int32)
        aux_edges = np.array(self.edges, dtype=np.int32)
        aux_edges = np.expand_dims(aux_edges, axis=-1) # para hace boradcasting
        
        out = aux_img - aux_edges

        # verificamos que no existan valores por debajo de 0
        out[out < 0] = 0
        return out

    def plot(self, save=False, name='edges'):
        # imagen original
        ax1 = plt.subplot(1,3,1)
        ax1.imshow(self.img)
        ax1.axis('off')
        ax1.set_title('Original')

        # bordes
        out = self.enhance()
        ax2 = plt.subplot(1,3,2)
        ax2.imshow(self.edges, cmap='gray')
        ax2.axis('off')
        ax2.set_title('Edges')

        # resultado
        ax3 = plt.subplot(1,3,3)
        ax3.imshow(out)
        ax3.axis('off')
        ax3.set_title('Result')

        if save:
            plt.savefig(f'plot_{name}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def imwrite(self, name='result'):
        out = self.enhance() # resultado en RGB
        out = np.array(out, dtype=np.uint8)
        out = cv.cvtColor(out, cv.COLOR_RGB2BGR) # transformacion a BGR
        cv.imwrite(f'{name}.png', out)