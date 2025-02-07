from typing import Any, Dict, List, Union
from env.src.entities import Inventory, Entity
from env.src.instance import FactorioInstance
from eval.tasks.task_abc import TaskABC
from env.src.utils.achievements import eval_program_with_achievements
from eval.open.model.game_state import GameState
import copy

LAB_PLAY_POPULATED_STARTING_INVENTORY = {"coal": 500, "burner-mining-drill": 10, "wooden-chest": 10, "burner-inserter": 10, "transport-belt": 500,
                                "stone-furnace": 10, "pipe": 10, "boiler": 4, "offshore-pump": 3, "steam-engine": 2,
                                "iron-gear-wheel": 22, "iron-plate": 19, "copper-plate": 52, "electronic-circuit": 99,
                                "iron-ore": 62, "stone": 50, "electric-mining-drill": 10, "small-electric-pole": 500, "pipe": 100,
                                "assembling-machine-1": 5}



class ThroughputTask(TaskABC):
    def __init__(self, maximum_steps, starting_inventory: Union[Inventory, Dict], task: str,
                  throughput_entity: Entity, quota: int, wait_period: int, starting_setup_code_location: str = None):
        super().__init__(maximum_steps, starting_inventory, task=task)
        self.throughput_entity = throughput_entity
        self.quota = quota
        self.wait_period = wait_period
        self.starting_setup_code_location = starting_setup_code_location
        self.starting_game_state = None
        self.starting_scenario_code = None
        self.starting_scenario_logs = None
    
    def verify(self, score: float, step: int, instance: FactorioInstance, step_statistics: Dict) -> bool:
        
        result, achievements, post_production_flows = eval_program_with_achievements(program = f"sleep({self.wait_period})", instance=instance)
        dynamic_achievements = achievements["dynamic"]
        return dynamic_achievements.get(self.throughput_entity.name, 0) >= self.quota, achievements
            
    def _to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "throughput_entity": self.throughput_entity,
            "quota": self.quota,
            "maximum_steps": self.maximum_steps,
            "starting_inventory": self.starting_inventory,
            "starting_setup_code_location": self.starting_setup_code_location,
            "initial_state": self.starting_game_state.to_raw(),
            "initial_scenario_code": self.starting_scenario_code,
            "initial_scenario_logs": self.starting_scenario_logs
        }


    def setup(self, instance, zero_game_state: GameState):
        """Code to provision the task environment"""
        reset_game_state_copy = copy.deepcopy(zero_game_state)
        reset_game_state_copy.inventory = self.starting_inventory
        instance.reset(reset_game_state_copy)
        print(instance.namespace.inspect_inventory())
        if self.starting_setup_code_location is None:
            starting_game_state = GameState.from_instance(instance)
            self.starting_game_state = starting_game_state
            return
        # read in the starting code
        with open(self.starting_setup_code_location, "r") as f:
            starting_code = f.read()
        # execute the starting code
        output_list, result, error, achievements = eval_program_with_achievements(instance, starting_code)
        # get the game state
        starting_game_state = GameState.from_instance(instance)
        self.starting_game_state = starting_game_state
        self.starting_scenario_code = starting_code
        self.starting_scenario_logs = result
