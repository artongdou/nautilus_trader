#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2024 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

# fmt: off

from playground.smc_strategy import SmartMoneyConceptStrategy, SmartMoneyConceptStrategyConfig
from nautilus_trader.adapters.interactive_brokers.config import IBMarketDataTypeEnum
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersDataClientConfig
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersExecClientConfig
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersInstrumentProviderConfig
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveDataClientFactory
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveExecClientFactory
from nautilus_trader.config import LiveDataEngineConfig
from nautilus_trader.config import LoggingConfig
from nautilus_trader.config import RoutingConfig
from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.examples.strategies.subscribe import SubscribeStrategy
from nautilus_trader.examples.strategies.subscribe import SubscribeStrategyConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.data import BarType
from nautilus_trader.model.data import BarSpecification
from nautilus_trader.model.enums import AggregationSource
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import PriceType

import os
from dotenv import load_dotenv


# fmt: on

# *** THIS IS A TEST STRATEGY WITH NO ALPHA ADVANTAGE WHATSOEVER. ***
# *** IT IS NOT INTENDED TO BE USED TO TRADE LIVE WITH REAL MONEY. ***

# *** THIS INTEGRATION IS STILL UNDER CONSTRUCTION. ***
# *** CONSIDER IT TO BE IN AN UNSTABLE BETA PHASE AND EXERCISE CAUTION. ***

load_dotenv()

instrument_provider = InteractiveBrokersInstrumentProviderConfig(
    load_ids=frozenset(
        [
            # "EUR/USD.IDEALPRO",
            "BTC/USD.PAXOS",
            "SPY.ARCA",
            # "AAPL.NASDAQ",
            # "V.NYSE",
            # "CLZ28.NYMEX",
            # "ESZ28.CME",
        ],
    ),
)

# Configure the trading node

config_node = TradingNodeConfig(
    trader_id="TESTER-001",
    logging=LoggingConfig(log_level="INFO", log_level_file="INFO"),
    data_clients={
        "IB": InteractiveBrokersDataClientConfig(
            ibg_host="127.0.0.1",
            ibg_port=int(os.getenv("PAPER_PORT")),
            ibg_client_id=1,
            handle_revised_bars=False,
            use_regular_trading_hours=True,
            # market_data_type=IBMarketDataTypeEnum.DELAYED_FROZEN,  # If unset default is REALTIME
            instrument_provider=instrument_provider,
        ),
    },
    exec_clients={
        "IB": InteractiveBrokersExecClientConfig(
            ibg_host="127.0.0.1",
            ibg_port=int(os.getenv("PAPER_PORT")),
            ibg_client_id=1,
            account_id=os.getenv(
                "PAPER_ACCOUNT_NUMBER"
            ),  # This must match with the IB Gateway/TWS node is connecting to
            instrument_provider=instrument_provider,
            routing=RoutingConfig(
                default=True,
            ),
        ),
    },
    data_engine=LiveDataEngineConfig(
        time_bars_timestamp_on_close=False,  # Will use opening time as `ts_event` (same like IB)
        validate_data_sequence=True,  # Will make sure DataEngine discards any Bars received out of sequence
    ),
    timeout_connection=90.0,
    timeout_reconciliation=5.0,
    timeout_portfolio=5.0,
    timeout_disconnection=5.0,
    timeout_post_stop=2.0,
)


# Instantiate the node with a configuration
node = TradingNode(config=config_node)

# Configure your strategy
# strategy_config = SubscribeStrategyConfig(
#     instrument_id=InstrumentId.from_str("BTC/USD.PAXOS"),
#     trade_ticks=False,
#     quote_ticks=False,
#     bars=True,
# )
instrument_id = InstrumentId.from_str("SPY.ARCA")
# instrument_id = InstrumentId.from_str("BTC/USD.PAXOS")
strategy_config = SmartMoneyConceptStrategyConfig(
    instrument_id=instrument_id,
    bar_type=BarType(
        instrument_id=instrument_id,
        bar_spec=BarSpecification(
            step=1,
            aggregation=BarAggregation.MINUTE,
            price_type=PriceType.LAST,
        ),
        aggregation_source=AggregationSource.INTERNAL,
    ),
)
# Instantiate your strategy
strategy = SmartMoneyConceptStrategy(config=strategy_config)

# Add your strategies and modules
node.trader.add_strategy(strategy)

# Register your client factories with the node (can take user-defined factories)
node.add_data_client_factory("IB", InteractiveBrokersLiveDataClientFactory)
node.add_exec_client_factory("IB", InteractiveBrokersLiveExecClientFactory)
node.build()


# Stop and dispose of the node with SIGINT/CTRL+C
if __name__ == "__main__":
    try:
        node.run()
    finally:
        node.dispose()
