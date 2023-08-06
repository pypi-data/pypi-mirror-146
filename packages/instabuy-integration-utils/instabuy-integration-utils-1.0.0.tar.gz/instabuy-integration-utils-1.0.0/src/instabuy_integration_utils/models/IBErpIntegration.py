from abc import abstractmethod


class IBErpIntegration:

    @staticmethod
    @abstractmethod
    def update_prices_and_stocks():
        pass

    @staticmethod
    @abstractmethod
    def sync_buys():
        pass
