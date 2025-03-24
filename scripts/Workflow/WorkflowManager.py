from .MSConvertWorkflow import MSConvertWorkflow
from .TopfdWorkflow import TopfdWorkflow
from .ToppicWorkflow import ToppicWorkflow
from .TopmgWorkflow import TopmgWorkflow
from .PbfgenWorkflow import PbfgenWorkflow
from .PromexWorkflow import PromexWorkflow
from .MSpathfinderWorkflow import MSpathfinderWorkflow
from .PbfgenPromexWorkflow import PbfgenPromexWorkflow
from .ToppicSuitWorkflow import ToppicSuitWorkflow
from .SpectrumSumWorkflow import SpectrumSumWorkflow

class WorkflowManager:
    @staticmethod
    def create_workflow(mode, args):
        workflows = {
            'msconvert': MSConvertWorkflow,
            'topfd': TopfdWorkflow,
            'toppic': ToppicWorkflow,
            'topmg': TopmgWorkflow,
            'pbfgen': PbfgenWorkflow,
            'promex': PromexWorkflow,
            'mspathfinder': MSpathfinderWorkflow,
            'pbfgen and promex': PbfgenPromexWorkflow,
            'toppic suit': ToppicSuitWorkflow,
            'sum spectrum': SpectrumSumWorkflow,
            # 可以添加更多模式
        }
        
        if mode not in workflows:
            raise ValueError(f"不支持的模式: {mode}")
            
        return workflows[mode](args) 

if __name__ == '__main__':
    pass
