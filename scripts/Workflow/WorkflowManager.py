from .OnlyConvertWorkflow import OnlyConvertWorkflow
from .OnlyTopfdWorkflow import OnlyTopfdWorkflow
from .OnlyToppicWorkflow import OnlyToppicWorkflow
from .ToppicWorkflow import ToppicWorkflow

class WorkflowManager:
    @staticmethod
    def create_workflow(mode, args):
        workflows = {
            'only convert': OnlyConvertWorkflow,
            'only topfd': OnlyTopfdWorkflow,
            'only toppic': OnlyToppicWorkflow,
            'toppic': ToppicWorkflow,
            # 可以添加更多模式
        }
        
        if mode not in workflows:
            raise ValueError(f"不支持的模式: {mode}")
            
        return workflows[mode](args) 

if __name__ == '__main__':
    pass
