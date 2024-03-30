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


from nautilus_trader.adapters.bybit.common.enums import BybitInstrumentType


def get_http_base_url(is_testnet: bool) -> str:
    if is_testnet:
        return "https://api-testnet.bybit.com"
    else:
        return "https://api.bytick.com"


def get_ws_base_url_public(
    instrument_type: BybitInstrumentType,
    is_testnet: bool,
) -> str:
    if not is_testnet:
        if instrument_type == BybitInstrumentType.SPOT:
            return "wss://stream.bybit.com/v5/public/spot"
        elif instrument_type == BybitInstrumentType.LINEAR:
            return "wss://stream.bybit.com/v5/public/linear"
        elif instrument_type == BybitInstrumentType.INVERSE:
            return "wss://stream.bybit.com/v5/public/inverse"
        elif instrument_type == BybitInstrumentType.OPTION:
            return "wss://stream.bybit.com/v5/public/option"
        else:
            raise RuntimeError(
                f"invalid `BybitAccountType`, was {instrument_type}",  # pragma: no cover
            )
    else:
        if instrument_type == BybitInstrumentType.SPOT:
            return "wss://stream-testnet.bybit.com/v5/public/spot"
        elif instrument_type == BybitInstrumentType.LINEAR:
            return "wss://stream-testnet.bybit.com/v5/public/linear"
        elif instrument_type == BybitInstrumentType.INVERSE:
            return "wss://stream-testnet.bybit.com/v5/public/inverse"
        elif instrument_type == BybitInstrumentType.OPTION:
            return "wss://stream-testnet.bybit.com/v5/public/option"
        else:
            raise RuntimeError(f"invalid `BybitAccountType`, was {instrument_type}")


def get_ws_base_url_private(is_testnet: bool) -> str:
    if is_testnet:
        return "wss://stream-testnet.bybit.com/v5/private"
    else:
        return "wss://stream.bybit.com/v5/private"
