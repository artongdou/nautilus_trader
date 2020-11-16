# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2020 Nautech Systems Pty Ltd. All rights reserved.
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

from cpython.datetime cimport datetime

from nautilus_trader.data.client cimport DataClient
from nautilus_trader.model.c_enums.bar_aggregation cimport BarAggregation
from nautilus_trader.model.c_enums.price_type cimport PriceType
from nautilus_trader.model.identifiers cimport Symbol
from nautilus_trader.model.instrument cimport Instrument
from nautilus_trader.model.tick cimport Tick
from nautilus_trader.model.tick cimport QuoteTick
from nautilus_trader.model.tick cimport TradeTick


cdef class BacktestDataContainer:
    cdef readonly set symbols
    cdef readonly dict instruments
    cdef readonly dict quote_ticks
    cdef readonly dict trade_ticks
    cdef readonly dict bars_bid
    cdef readonly dict bars_ask

    cpdef void add_instrument(self, Instrument instrument) except *
    cpdef void add_quote_ticks(self, Symbol symbol, data) except *
    cpdef void add_trade_ticks(self, Symbol symbol, data) except *
    cpdef void add_bars(self, Symbol symbol, BarAggregation aggregation, PriceType price_type, data) except *
    cpdef void check_integrity(self) except *
    cpdef long total_data_size(self)


cdef class BacktestDataClient(DataClient):
    cdef BacktestDataContainer _data
    cdef object _quote_tick_data
    cdef object _trade_tick_data

    cdef dict _symbol_index

    cdef unsigned short[:] _quote_symbols
    cdef list _quote_bids
    cdef list _quote_asks
    cdef list _quote_bid_sizes
    cdef list _quote_ask_sizes
    cdef datetime[:] _quote_timestamps
    cdef dict _quote_symbol_index
    cdef int _quote_index
    cdef int _quote_index_last

    cdef unsigned short[:] _trade_symbols
    cdef list _trade_prices
    cdef list _trade_sizes
    cdef list _trade_match_ids
    cdef list _trade_makers
    cdef datetime[:] _trade_timestamps
    cdef dict _trade_symbol_index
    cdef int _trade_index
    cdef int _trade_index_last

    cdef TradeTick _next_trade_tick
    cdef QuoteTick _next_quote_tick

    cdef readonly list execution_resolutions
    cdef readonly datetime min_timestamp
    cdef readonly datetime max_timestamp
    cdef readonly bint has_data

    cpdef void setup(self, datetime start, datetime stop) except *
    cpdef void reset(self) except *
    cdef Tick next_tick(self)

    cdef inline QuoteTick _generate_quote_tick(self, int index)
    cdef inline TradeTick _generate_trade_tick(self, int index)
    cdef inline void _iterate_quote_ticks(self) except *
    cdef inline void _iterate_trade_ticks(self) except *
