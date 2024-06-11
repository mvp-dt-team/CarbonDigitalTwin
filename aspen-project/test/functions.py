from CodeLibraryCustom import Simulation
import os

working_path = os.getcwd()

## на вход принимаются разные файлы для двух кейсов
sim = Simulation(
    AspenFileName="Styrene.bkp",
    WorkingDirectoryPath=working_path + "\\schemes",
    VISIBILITY=False,
)


def calculation_column_params(amountEB, simulation):
    simulation.STRM_Set_TotalFlowBasis(
        Streamname="10-FEED", TotalFlowBasis=amountEB, Compoundname="ETHYLBEN"
    )
    simulation.Run()
    col11_out = simulation.BLK_RADFRAC_GET_OUTPUTS("COL11")
    col21_out = simulation.BLK_RADFRAC_GET_OUTPUTS("COL21")
    return (
        col11_out["Condenser_RefluxRatio"],
        col11_out["Reboiler_BottomsToFeedRatio"],
        col21_out["Reboiler_BottomsToFeedRatio"],
    )


calculation_column_params(50, sim)
sim.CloseAspen()

# working_path = os.getcwd()
sim = Simulation(
    AspenFileName="StyreneWithoutOptimizer.bkp",
    WorkingDirectoryPath=os.path.join(working_path, "schemes2"),
    VISIBILITY=False,
)


def calculation_flow_composition(
    reflux_ratio: float, bottoms_to_feed_ratio: float, simulation
):
    cases = {
        "60-VAPOR": [
            "ETHYLBEN",
            "TOLUENE",
            "BENZENE",
            "STYRENE",
            "ETHYLENE",
            "HYDROGEN",
            "METHANE",
            "WATER",
        ],
        "56-ORGAN": [
            "ETHYLBEN",
            "TOLUENE",
            "BENZENE",
            "STYRENE",
            "ETHYLENE",
            "HYDROGEN",
            "METHANE",
            "WATER",
        ],
        "64-STYRE": [
            "ETHYLBEN",
            "TOLUENE",
            "BENZENE",
            "STYRENE",
            "ETHYLENE",
            "HYDROGEN",
            "METHANE",
            "WATER",
        ],
        "62-ORGAN": [
            "ETHYLBEN",
            "TOLUENE",
            "BENZENE",
            "STYRENE",
            "ETHYLENE",
            "HYDROGEN",
            "METHANE",
            "WATER",
        ],
    }
    simulation.BLK_RADFRAC_Set_Refluxratio("COL11", reflux_ratio)
    simulation.BLK_RADFRAC_Set_BottomToFeedRatio("COL11", bottoms_to_feed_ratio)
    simulation.Run()
    result = {}
    for stream in cases:
        result[stream] = {}
        result[stream]["Общее"] = simulation.STRM_Get_MassFlowMixed(stream)
        for compound in cases[stream]:
            result[stream][compound] = simulation.STRM_Get_MassFracPerCompound(
                stream, compound
            )


calculation_flow_composition(50, 0.6, sim)
sim.CloseAspen()
