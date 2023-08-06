from typing import Dict, Optional, Union, List
import numpy as np
import pandas as pd

from quickstats.plots import AbstractPlot
from quickstats.plots.template import create_transform
from quickstats.utils.common_utils import combine_dict
from matplotlib.lines import Line2D

class Likelihood2DPlot(AbstractPlot):
    
    CONFIG = {
        'sigma_levels': ('1sigma', '2sigma', '3sigma'),
        'sigma_pos': 0.93,
        'sigma_names': ('1 $\sigma$', '2 $\sigma$', '3 $\sigma$'),
        'sigma_colors': ("hh:darkblue", "#F2385A", "#FDC536"),
        'highlight_styles': {
            'linewidth' : 0,
            'marker' : '*',
            'markersize' : 20,
            'color' : '#E9F1DF',
            'markeredgecolor' : 'black'
        }
    }
    # https://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf#page=31
    likelihood_label_threshold = {
        '1sigma': ('1 $\sigma$', 2.30),
        '0.90': ('90%', 4.61),
        '0.95': ('95%', 5.99),
        '2sigma': ('2 $\sigma$', 6.18),
        '0.99': ('99%', 9.21),
        '3sigma': ('3 $\sigma$', 11.83),
    }

    
    def __init__(self, data_map:Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map:Optional[Dict]=None,
                 styles_map:Optional[Dict]=None,
                 color_cycle=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        
        self.data_map = data_map
        self.label_map = label_map
        self.styles_map = styles_map
        self.highlight_data = []
        self.legend_order = []
        
        super().__init__(color_cycle=color_cycle,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        
    def get_default_legend_order(self):
        if not isinstance(self.data_map, dict):
            return self.legend_order
        else:
            return list(self.data_map)
        
    def draw_single_data(self, ax, data:pd.DataFrame, 
                         styles:Optional[Dict]=None,
                         xattrib:str='klambda', yattrib:str='k2v', zattrib:str='nll', clabel_size=None):
        colors = ['k'] + list(self.config['sigma_colors'])
        levels = [0] + [self.likelihood_label_threshold[key][1] for key in self.config['sigma_levels']]
        x = data[xattrib]
        y = data[yattrib]
        X_unique = np.sort(self.data_map[xattrib].unique())
        Y_unique = np.sort(self.data_map[yattrib].unique())
        X, Y = np.meshgrid(X_unique, Y_unique)
        Z = self.data_map.pivot_table(index=xattrib, columns=yattrib, values=zattrib).T.values - self.data_map[zattrib].min()

        cp = ax.contour(X, Y, Z, levels=levels, colors=colors, linewidths=2)
        if clabel_size is not None:
            ax.clabel(cp, inline=True, fontsize=clabel_size)
        custom_handles = [Line2D([0], [0], color=color, lw=2, label=self.likelihood_label_threshold[key][0]) for color, key in zip(self.config['sigma_colors'], self.config['sigma_levels'])]
        ax.legend(handles=custom_handles, **self.styles['legend'])
        self.update_legend_handles(dict(zip(self.config['sigma_levels'], custom_handles)))
        self.legend_order.extend(self.config['sigma_levels'])

        return custom_handles
    
    def draw(self, xattrib:str='klambda', yattrib:str='k2v', zattrib:str='nll', xlabel:Optional[str]="$\kappa_\lambda$", 
             ylabel:Optional[str]="$\kappa_{2v}$", zlabel:Optional[str]="$-2\Delta ln(L)$",
             ymax:float=5, ymin:float=-5, xmin:Optional[float]=-10, xmax:Optional[float]=10, clabel_size=None, draw_sm_line:bool=False):
        ax = self.draw_frame()
        if isinstance(self.data_map, pd.DataFrame):
            self.draw_single_data(ax, self.data_map, self.styles_map,
                                  xattrib=xattrib, yattrib=yattrib, clabel_size=clabel_size)
        elif isinstance(self.data_map, dict):
            assert(0), "not implemented"
            if self.styles_map is None:
                styles_map = {k:None for k in self.data_map}
            else:
                styles_map = self.styles_map
            if self.label_map is None:
                label_map = {k:k for k in data_map}
            else:
                label_map = self.label_map
            handles = {}
            for key in self.data_map:
                data = self.data_map[key]
                styles = styles_map.get(key, None)
                label = label_map.get(key, "")
                handle = self.draw_single_data(ax, data, styles, 
                                               label=label,
                                               xattrib=xattrib,
                                               yattrib=yattrib,
                                               clabel_size=clabel_size
                                               )
                handles[key] = handle
            self.update_legend_handles(handles)
        else:
            raise ValueError("invalid data format")


        if self.highlight_data is not None:
            for i, h in enumerate(self.highlight_data):
                self.draw_highlight(ax, h, i)

        if draw_sm_line:
            sm_line_styles = self.config['sm_line_styles']
            sm_values = self.config['sm_values']
            transform = create_transform(transform_y="axis", transform_x="data")
            ax.vlines(sm_values[0], ymin=0, ymax=1, zorder=0, transform=transform,
                      **sm_line_styles)
            transform = create_transform(transform_x="axis", transform_y="data")
            ax.hlines(sm_values[1], xmin=0, xmax=1, zorder=0, transform=transform,
                      **sm_line_styles)

        handles, labels = self.get_legend_handles_labels()
        ax.legend(handles, labels, **self.styles['legend'])
        ax.set_ylim([ymin, ymax])
        ax.set_xlim([xmin, xmax])

        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        
        return ax

    def draw_highlight(self, ax, data, index=0):
        styles = data['styles']
        if styles is None:
            styles = self.config['highlight_styles']
        handle = ax.plot(data['x'], data['y'], label=data['label'], **styles)
        self.update_legend_handles({f'highlight_{index}': handle[0]})
        self.legend_order.append(f'highlight_{index}')
        

    def add_highlight(self, x:float, y:float, label:str="SM prediction",
                      styles:Optional[Dict]=None):
        highlight_data = {
            'x'     : x,
            'y'     : y,
            'label' : label,
            'styles': styles
        }
        self.highlight_data.append(highlight_data)
