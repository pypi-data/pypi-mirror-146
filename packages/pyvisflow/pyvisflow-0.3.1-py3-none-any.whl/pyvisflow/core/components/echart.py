from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvisflow.core.dataset.props import DatasetSeriesPropInfo, ReactiveDatasetPropInfo
from pyvisflow.core.props import SubscriptableTypePropInfo, StrTypePropInfo
from pyvisflow.core.props.absProp import AbsPropInfo


from .auto_create._echart import _EChart


class EChart(_EChart):
    def __init__(
            self,
    ) -> None:
        super().__init__()
        self._series = []
        (
            self
            .set_option('series',[])
        )

    @property
    def utils(self, ):
        return Helper(self)


    def set_option(self, prop: str, data: Any):
        if not prop.startswith('option.'):
            prop = f'option.{prop}'
        self.set_prop(prop, data)
        return self

    def set_series(self, idx: int, prop: str, data: Any):
        self.set_option(f'series[{idx}].{prop}', data)
        return self

    @property
    def clickInfo(self):
        p = self.get_prop('clickInfo')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)





    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()

        data.update({
            'option':{

            },
            'clickInfo': {},
        })
        return data


class Helper():
    def __init__(self, echart: EChart) -> None:
        self._echart = echart

    def use_from_option_dict(self,option:Dict):
        for key,value in option.items():
            self._echart.set_option(key,value)
        return self

    def use_pie(self, dataset: ReactiveDatasetPropInfo):

        dataset = dataset.rename({0:'name',1:'value'})[['name','value']]

      
        self._echart.set_option('series', [{
            'type': 'pie',
            'id': self._echart._id,
            "universalTransition": True,
        }]) \
        .set_option('legend', {
                                'top': '5%',
                                'left': 'center'
                            },) \
        .set_option('series[0].data',dataset.to_jsObject())
        return PieHelper(self._echart)

    def use_bar(self, x: AbsPropInfo, y: AbsPropInfo):
        self._echart.set_option('xAxis',{}).set_option('yAxis',{})
        self._echart.set_option('series', [{
            'type': 'bar',
            'showBackground': True,
            'backgroundStyle': {
                'color': 'rgba(180, 180, 180, 0.2)'
            },
            'encode': {
                'x': x,
                'y': y
            },
            'id': self._echart._id,
            "universalTransition": True,
        }]).set_option('xAxis', {'type': 'category'}).set_prop(
        'option.xAxis.data',x).set_prop(
        'option.series[0].data',y
        )



        return BarHelper(self._echart)

    def use_line(self, x: AbsPropInfo, y: AbsPropInfo, color: Optional[str] = None):
        self._echart.set_option('xAxis',{}).set_option('yAxis',{})
        self._echart.set_option('series', [{
            'type': 'line',
            'encode': {
                'x': x,
                'y': y,
                'color' :color
            },
            'id': self._echart._id,
            "universalTransition": True,
        }]) \
        .set_option('xAxis', {'type': 'category'}) \
        .set_option('yAxis', {'type': 'value'}) \
        .set_option('tooltip', {'trigger': 'axis'}) \
        .set_option('xAxis.data',x) \
        .set_option('series[0].data',y)
        return LineHelper(self._echart)


class AbsHelper():

    def __init__(self, echart: EChart) -> None:
        self._echart = echart

    def set_prop(self, prop: str, value: Union[AbsPropInfo, Any]):
        self._echart.set_prop(prop,value)
        return self

class LineHelper(AbsHelper):
    def __init__(self, echart: EChart) -> None:
        super().__init__(echart)

    def area_chart(self):
        '''
        基础面积图
        '''
        self._echart \
                    .set_series(0, 'areaStyle', {}) \
                    .set_series(0,'symbol','none') \
                    .set_series(0,'sampling','lttb') \
                    .set_series(0,  "lineStyle",{"width": 0}) \
                    .set_option('xAxis', {'type': 'category'})

        return self

    def smooth(self):
        '''
        平滑化
        '''
        self._echart \
                    .set_series(0, 'smooth', True) \

        return self


class BarHelper(AbsHelper):
    def __init__(self, echart: EChart) -> None:
        super().__init__(echart)

    def showBackground(self, color: str = 'rgba(180, 180, 180, 0.2)'):
        '''
        显示柱子背景
        '''
        self._echart \
                    .set_series(0, 'showBackground', True) \
                    .set_series(0, 'backgroundStyle',  {
                        'color': color
                    }) \

        return self


class PieHelper(AbsHelper):
    def __init__(self, echart: EChart) -> None:
        super().__init__(echart)

    def circle_chart(self):
        '''
        圆环图
        '''
        self._echart.set_series(0, 'labelLine', {
            'show': False
        }).set_series(0, 'emphasis', {
            'label': {
                'show': True,
                'fontSize': '40',
                'fontWeight': 'bold'
            }
        }).set_series(0, 'label', {
            'show': False,
            'position': 'center'
        }).set_series(0, 'itemStyle', {
            'borderRadius': 10,
            'borderColor': '#fff',
            'borderWidth': 2
        }).set_series(0, 'avoidLabelOverlap', False).set_series(
            0, 'radius', ['40%', '70%']).set_series(0, 'type', 'pie')

        return self

    def nightingale_rose_chart(self):
        '''
        南丁格尔玫瑰图
        '''
        self._echart \
                    .set_series(0, 'type', 'pie') \
                    .set_series(0, 'center',  ['50%', '50%']) \
                    .set_series(0, 'roseType', 'area') \
                    .set_series(0, 'itemStyle', {
                                                'borderRadius': 8
                                            }) \

        return self