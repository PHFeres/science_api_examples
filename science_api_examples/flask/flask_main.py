from science_api.flask import BaseResource, BaseApp

from science_api_examples.io.example_io import ExampleIO
from science_api_examples.io.example_verify import ExampleVerify


class GreeterResource(BaseResource):
    """

    @api {post} /railroad/simulate send simulation on integrated system
    @apiName PostSimulationParameters
    @apiGroup Railroad

    @apiParam (Input_json) {String} id Current simulation identification
    @apiParam (Input_json) {Int} init_date Timestamp related to the beginning of simulation
    @apiParam (Input_json) {Int} end_date Timestamp related to the end of simulation
    @apiParam (Input_json) {[Dict]} demands Information related to highroad flow
    @apiParam (Input_json) {[Dict]} vessels_all Information related to expected vessels (ships)
    @apiParam (Input_json) {[Dict]} maintenance Planned maintenance to happen in the simulation
    @apiParam (Input_json) {[Dict]} terminals Information of each terminal
    @apiParam (Input_json) {[Dict]} ports Information of each port
    @apiParam (Input_json) {Dict} railroad Information related to railroad, flows information
    @apiParam (Input_json) {[Dict]} third_terminals Information of each third terminal

    @apiParam (demands) {int} flow Id of each demand
    @apiParam (demands) {String = "soy", "soy_bran", "sugar", "corn"} product Current demand's product
    @apiParam (demands) {String} client Current demand's client
    @apiParam (demands) {String} origin Id of origin element (in the MVP must be a terminal)
    @apiParam (demands) {String} destiny Id of destiny element (in the MVP must be a port)
    @apiParam (demands) {dict} demand Information of maximum demand,
    @apiParam (demands) {[float]} demand[month_number] ton of product per week
    @apiParam (demands) {dict} min Information of minimum demand
    @apiParam (demands) {[float]} min[month_number] ton of product per week
    @apiParam (demands) {float} distance Information related to distance < TODO (feres) confirm >

    @apiParam (vessels_all) {String} port_id Identification of port that current vessel can dock
    @apiParam (vessels_all) {int} eta_min Timestamp of arrival date of current ship
    @apiParam (vessels_all) {int} eta_max Timestamp of departure date of current ship
    @apiParam (vessels_all) {bool} op_month Identifies if current ship is an initial state one
                                            (already starts simulation in some cradle)
    @apiParam (vessels_all) {String = "soy", "soy_bran", "sugar", "corn"} product Current vessel's product
    @apiParam (vessels_all) {int} volume Maximum volume that current ship can have
    @apiParam (vessels_all) {String} client Current ship client
    @apiParam (vessels_all) {String} name Ship's name

    @apiParam (maintenance) {String} instance_id The Id of the element where current maintenance will be made
    @apiParam (maintenance) {int} date Timestamp of maintenance start
    @apiParam (maintenance) {int} unavailable_hours Number of hours that maintenance will last
    @apiParam (maintenance) {String} reason Maintenance's reason (to be printed)
    @apiParam (maintenance) {String = null, "storage", "receive", "expedition"} type Maintenance's type
    @apiParam (maintenance) {int} max_vol_allowed    < TODO (Feres) complete >
    @apiParam (maintenance) {String = null} allowed_products
    @apiParam (maintenance) {[int]} capacity_multipliers
    @apiParam (maintenance) {[int]} rates_multipliers

    @apiParam (terminals) {String} id Terminal's identification
    @apiParam (terminals) {[Dict]} rates Information related to terminal's expedition and receive rates
    @apiParam (terminals) {String = "soy", "soy_bran", "sugar", "corn"} rates[product] Product of current rate
    @apiParam (terminals) {String = "receive", "expedition"} rates[operation] Identifies which operation this
                                                                              element is about
    @apiParam (terminals) {String = "road", "railroad"} rates[modal] Identifies current element modal
    @apiParam (terminals) {[float]{7}} rates[limit] Value of operation's rate for each day of the week
    @apiParam (terminals) {[Dict]} warehouses Information related to terminal's warehouses
    @apiParam (terminals) {Dict} initial_stock Information related to turnover stock of current terminal
                                               (stock in the beginning of simulation)

    @apiParam (ports) {String} id Port's identification
    @apiParam (ports) {[String = "soy", "soy_bran", "sugar", "corn"]} fiscal_pool Products which the fiscal pool rule
                                                                                  applies
    @apiParam (ports) {[Dict]} mill_hoppers Mill hopper related information
    @apiParam (ports) {Dict} initial_stock Information related to turnover stock of current terminal
                                           (stock in the beginning of simulation)
    @apiParam (ports) {[Dict]} cradles Cradle related information
    @apiParam (ports) {Dict} tide Information related to simulation tides in current port
    @apiParam (ports) {[Dict]} warehouses Information related to terminal's warehouses

    @apiParam (third_ports) {String} id Third port's identification
    @apiParam (third_ports) {[Dict]} capacity Information related to operation rates
    @apiParam (third_ports) {String = "soy", "soy_bran", "sugar", "corn"} capacity[product] Element's
                                                                                            product information
    @apiParam (third_ports) {String = "receive", "storage"} capacity[operation] Information related to
                                                                                element's operation
    @apiParam (third_ports) {[int]{7}} capacity[wagons] Number of wagons for current rate element
                                                        (for each week day, beginning in sunday)

    @apiParam (third_terminals) {String} id Third terminal's identification
    @apiParam (third_terminals) {[Dict]} capacity Information related to operation rates
    @apiParam (third_terminals) {String = "soy", "soy_bran", "sugar", "corn"} capacity[product] Element's
                                                                                                product information
    @apiParam (third_terminals) {String = "receive", "storage"} capacity[operation] Information related to
                                                                                    element's operation
    @apiParam (third_terminals) {[int]{7}} capacity[wagons] Number of wagons for current rate element
                                                           (for each week day, beginning in sunday)


    @apiParam (railroad) {[Dict]} wagons_per_train Information related to number of wagons in each train
    @apiParam (railroad) {String = "soy", "soy_bran", "sugar", "corn"} wagons_per_train[product] Product of current
                                                                                                 information
    @apiParam (railroad) {int} wagons_per_train[max_wagons] Number of wagons in a train

    @apiParam (railroad) {[Dict]} initial_fleet Information related to initial conditions of trains

    @apiParam (railroad) {[Dict]} exchange Information related to exchange module
    @apiParam (railroad) {[Dict]} exchange[destiny] Identification of port attached to this module,
                                                    must match Id of a port
    @apiParam (railroad) {int} exchange[max_trains]     TODO (feres) complete
    @apiParam (railroad) {int} exchange[day_interval]

    @apiParam (railroad) {[Dict]} premise Information related to wagons' weight
    @apiParam (railroad) {String = "soy", "soy_bran", "sugar", "corn"} premise[product] Product of current element
    @apiParam (railroad) {String} premise[origin] Identification of origin, must match a terminal's Id
    @apiParam (railroad) {float} premise[capacity] Weight of each wagon (ton)


    @apiParam (railroad) {[Dict]} cycles Information related to cycles between terminal and ports
    @apiParam (railroad) {[Dict]} migration Information related to wagons' migration among fleets
    @apiParam (railroad) {String} migration[fleet_origin] Identification of fleet the wagons will be removed,
                                                          must match the ones in cycles
    @apiParam (railroad) {String} migration[fleet_destiny] Identification of fleet the wagons will be added,
                                                           must match the ones in cycles
    @apiParam (railroad) {int} migration[n_wagons] Number of wagons to be migrated
    @apiParam (railroad) {int} migration[time] Time to accomplish the migration (hours)     TODO (Feres) confirm
    @apiParam (railroad) {int} migration[init_date] Timestamp to inform when the migration will begin

    @apiParam (warehouses) {String} id Current warehouse identification
    @apiParam (warehouses) {[Dict]} cells Information related to cells of current warehouse

    @apiParam (cells) {String} id Current cell identification
    @apiParam (cells) {int} last_reset Timestamp of the last time current cell was empty
    @apiParam (cells) {Dict} setup Information related to time spent to change product in cell
    @apiParam (cells) {Dict} capacity Information related to cell's capacity
    @apiParam (cells) {[[]int]} capacity[product] First element is a list with minimum and maximum capacity for
                                                       current product, second element is TODO (Feres) complete

    @apiParam (initial_stock) {Dict} product Information related to current product (as key)
    @apiParam (initial_stock) {int} product[client] Ton of this product related to current client (as key)

    @apiParam (initial_fleet) {String} fleet Current fleet identification
    @apiParam (initial_fleet) {int} total_wagons Total number of wagons attached to this fleet
    @apiParam (initial_fleet) {[Dict]} full Information related to wagons initially full
    @apiParam (initial_fleet) {String = "soy", "soy_bran", "sugar", "corn"} full[product] Product of current element
    @apiParam (initial_fleet) {String} full[origin] Identification of origin, must match a terminal's Id (in the MVP)
    @apiParam (initial_fleet) {String} full[destiny] Identification of destiny, must match a port's Id (in the MVP)
    @apiParam (initial_fleet) {float} full[value = [0,100]] percentage of the total wagons in this element

    @apiParam (cycles) {String} fleet Identification of fleet (must match the one in initial_fleet)
    @apiParam (cycles) {String = "soy", "soy_bran", "sugar", "corn"} product Current element's product
    @apiParam (cycles) {Dict} base Other information

    @apiParam (base) {String} origin Identification of origin, must match a terminal's Id (in the MVP)
    @apiParam (base) {String} destiny Identification of destiny, must match a port's Id (in the MVP)
    @apiParam (base) {Dict} times Information related to time (everything in hours) Todo (feres) confirm
    @apiParam (base) {Dict} times[full] Information related to full wagons
    @apiParam (base) {Dict} times[empty] Information related to empty wagons

    @apiParam (full / empty) {String = "loco_wait", "change_loco"} type Current cycle's type
    @apiParam (full / empty) {[float]} origin Times spent in the origin yard
    @apiParam (full / empty) {[float]} destiny Times spent in the destiny yard
    @apiParam (full / empty) {[Dict]} transit Times in railroad
    @apiParam (full / empty) {String} transit[origin] Identification of origin's station
    @apiParam (full / empty) {String} transit[destiny] Identification of destiny's station
    @apiParam (full / empty) {float} transit[time] hours spent from one station to the other

    @apiSuccess {Dict} port Information related to each port (separated by Id, third not considered)
    @apiSuccess {[[Dict]]} port.Id.stockByCell Information of each cell, uses basic return element
    @apiSuccess {[[Dict]]} port.Id.stockByWarehouse Information of each warehouse, uses basic return element
    @apiSuccess {[Dict]} port.Id.stockByPort Information of port total stock, uses basic return element
    @apiSuccess {[[Dict]]} port.Id.dockedInfo Information related to vessels that were docked in the simulation,
                                              uses vessel information format
    @apiSuccess {[[Dict]]} port.Id.notDockedInfo Information related to vessels that weren't docked in the simulation,
                                                 uses vessel information format
    @apiSuccess {[[Dict]]} port.Id.tideInfo Information related to tides during simulation
    @apiSuccess {int} port.Id.tideInfo.st_time Simulation's instant (closed interval)
    @apiSuccess {int} port.Id.tideInfo.end_time Simulation's instant (open interval)
    @apiSuccess {String = "low", "high", "unknown", "maintenance"} port.Id.tideInfo.value Tide value,
                                                                                          already interpreted
    @apiSuccess {[[Dict]]} port.Id.maintenanceInfo Information related to maintenance in cradles
    @apiSuccess {String} port.Id.maintenanceInfo.reason Maintenance's reason, has received in input
    @apiSuccess {int} port.Id.maintenanceInfo.duration Maintenance's duration (hours)
    @apiSuccess {int} port.Id.maintenanceInfo.init_timestamp Timestamp of maintenance begin
    @apiSuccess {int} port.Id.maintenanceInfo.end_timestamp Timestamp of maintenance end
    @apiSuccess {int} port.Id.maintenanceInfo.init_time Simulation instant of maintenance begin
    @apiSuccess {int} port.Id.maintenanceInfo.end_time Simulation instant of maintenance end
    @apiSuccess {[[Dict]]} port.Id.operatedVolume Information related to demand and operation of each product

    @apiSuccess {[[Dict]]} terminal Information related to each terminal (separated by Id, third not considered)
    @apiSuccess {[[Dict]]} terminal.Id.stockByCell Information of each cell, uses basic return element
    @apiSuccess {[[Dict]]} terminal.Id.stockByWarehouse Information of each warehouse, uses basic return element
    @apiSuccess {[Dict]} terminal.Id.stockByTerminal Information of terminal's total stock, uses basic return element
    @apiSuccess {[Dict]} terminal.Id.operatedVolume Information related to demand and operation of each product
    @apiSuccess {[Dict]} terminal.Id.cutByProduct Information related to product cuts, uses basic return element

    @apiSuccess {Dict} Railroad Information related to railroad operation
    @apiSuccess {Dict} Railroad.months Information divided by each month, keys are the month numbers (as string)
    @apiSuccess {Dict} Railroad.months.number Final dict information for current month number, uses railroad information

    @apiSuccess (Railroad information) {[Dict]} needed_wagons Information related to used wagons
    @apiSuccess (Railroad information) {String} needed_wagons.fleet Fleet's identification
    @apiSuccess (Railroad information) {String  = "soy", "soy_bran", "sugar", "corn"} needed_wagons.product Current
                                                                                       element product
    @apiSuccess (Railroad information) {String} needed_wagons.origin Identification of a origin element (terminal)
    @apiSuccess (Railroad information) {String} needed_wagons.destination Identification of a destiny element (port)
    @apiSuccess (Railroad information) {[Dict]} needed_wagons.need Numerical information of current element
    @apiSuccess (Railroad information) {Dict} needed_wagons.need.loaded Information related to full wagons
    @apiSuccess (Railroad information) {int} needed_wagons.need.loaded.wagons TODO (Feres) complete
    @apiSuccess (Railroad information) {int} needed_wagons.need.loaded.percentage
    @apiSuccess (Railroad information) {Dict} needed_wagons.need.empty Information related to empty wagons
    @apiSuccess (Railroad information) {int} needed_wagons.need.empty.wagons
    @apiSuccess (Railroad information) {int} needed_wagons.need.empty.percentage
    @apiSuccess (Railroad information) {int} needed_wagons.need.scheduled
    @apiSuccess (Railroad information) {[Dict]} trains_interval Information related to
    @apiSuccess (Railroad information) {String} trains_interval.fleet Fleet's identification
    @apiSuccess (Railroad information) {String  = "soy", "soy_bran", "sugar", "corn"} trains_interval.product Current
                                                                                       element product
    @apiSuccess (Railroad information) {String} trains_interval.origin Identification of a origin element (terminal)
    @apiSuccess (Railroad information) {String} trains_interval.destination Identification of a destiny element (port)
    @apiSuccess (Railroad information) {Dict} trains_interval.train_pair_month
    @apiSuccess (Railroad information) {float} trains_interval.train_pair_month.budgeted
    @apiSuccess (Railroad information) {float} trains_interval.train_pair_month.scheduled
    @apiSuccess (Railroad information) {Dict} trains_interval.weekly_opening
    @apiSuccess (Railroad information) {[float]} trains_interval.weekly_opening.weeks
    @apiSuccess (Railroad information) {float} trains_interval.trains_interval
    @apiSuccess (Railroad information) {[Dict]} opVol Information related to operated volume
    @apiSuccess (Railroad information) {String  = "soy", "soy_bran", "sugar", "corn"} opVol.product Current
                                                                                       element product
    @apiSuccess (Railroad information) {String} opVol.origin Identification of a origin element (terminal)
    @apiSuccess (Railroad information) {String} opVol.destination Identification of a destiny element (port)
    @apiSuccess (Railroad information) {String} opVol.flow TODO (Feres) complete
    @apiSuccess (Railroad information) {String} opVol.demand
    @apiSuccess (Railroad information) {String} opVol.operated
    @apiSuccess (Railroad information) {String} opVol.min

    @apiSuccess (Basic return element) {String} title Information to identify current element
    @apiSuccess (Basic return element) {String} xlabel Information related to x axis
    @apiSuccess (Basic return element) {String} ylabel Information related to y axis
    @apiSuccess (Basic return element) {[Dict]} data Contains numerical information
    @apiSuccess (Basic return element) {String} data.name Information related to variable to be shown
    @apiSuccess (Basic return element) {String = "line", "bar"} data.type Information of how to show this variable
    @apiSuccess (Basic return element) {[Dict]} data.data Numerical information
    @apiSuccess (Basic return element) {int} data.date Timestamp information
    @apiSuccess (Basic return element) {float} data.value Variable's value in informed timestamp

    @apiSuccess (Vessel information) {int} id Vessel's identification
    @apiSuccess (Vessel information) {String} name Vessel's name
    @apiSuccess (Vessel information) {int} eta
    @apiSuccess (Vessel information) {String = "soy", "soy_bran", "sugar", "corn"} product Vessel's product
    @apiSuccess (Vessel information) {String} client Vessel's client
    @apiSuccess (Vessel information) {int} volume_demand TODO (Feres) complete
    @apiSuccess (Vessel information) {int} volume
    @apiSuccess (Vessel information) {int} dock_time Simulation's dock instant
    @apiSuccess (Vessel information) {int} undock_time Simulation's undock instant
    @apiSuccess (Vessel information) {float} commercial_rate
    @apiSuccess (Vessel information) {int} dock_timestamp Timestamp of dock
    @apiSuccess (Vessel information) {int} undock_timestamp Timestamp of undock

    @apiSuccess (operatedVolume) {String = "soy", "soy_bran", "sugar", "corn"} product Product of current
                                                                                       element information
    @apiSuccess (operatedVolume) {int} demand TODO (Feres) complete
    @apiSuccess (operatedVolume) {int} expedition
    @apiSuccess (operatedVolume) {float} reception
    @apiSuccess (operatedVolume) {float} cut
    @apiSuccess (operatedVolume) {float} [embarkation]
    @apiSuccess (operatedVolume) {int} [disembarkation]


    """

    def __init__(self):
        """
        Declares each expected input of the JSON file
        """

        super().__init__()

        # Test argument
        self.parser.add_argument('people', required=True, type=dict, action="append")

        # this argument MUST NOT be removed, the queue Watcher uses it
        self.parser.add_argument('id', required=True, type=str)

    def post(self):
        """
        Executes simulation
        Returns: JSON output file

        """

        return self.aux_post(verification_class=ExampleVerify, io_class=ExampleIO)


base_app = BaseApp()
base_app.add_route(GreeterResource, "/greet")

if __name__ == '__main__':

    host_string = "0.0.0.0"

    base_app.run(ip_host=host_string)
