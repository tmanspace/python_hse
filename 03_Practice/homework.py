from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class TransactionType(Enum):
    DEPOSIT = 'Депозит'
    WITHDRAW = 'Снятие'
    INITIAL = 'Начальный'
    CANCELATION = 'Отмена'


@dataclass
class Transaction:
    '''Объект транзакции'''
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))  
    operation: TransactionType = TransactionType.INITIAL
    amount: float = 0.0
    date: datetime = field(default_factory=datetime.now)
    balance_after: float = 0.0

    def __str__(self):
        return f'{self.date.strftime('%Y-%m-%d %H:%M:%S')} - {self.operation.value.capitalize()} - {self.amount} - Баланс: {self.balance_after}'


@dataclass
class OperationResult:
    '''Результат операции'''
    transaction_id: str
    balance_after: float 
    message: str 

    def __str__(self):
        return f'ID транзакции: {self.transaction_id} | Баланс: {self.balance_after} | {self.message}'


class Account:

    def __init__(self, name: str, initial_balance: float = 0.0):
        self.name = name
        self.__balance = initial_balance
        self._transactions: list[Transaction] = []
        self._add_transaction(TransactionType.INITIAL, initial_balance)

    def deposit(self, amount: float) -> OperationResult:
        if amount <= 0:
            return OperationResult('', self.__balance, 'Нельзя добавить отрицательное значение.')
        self.__balance += amount
        transaction = self._add_transaction(TransactionType.DEPOSIT, amount)
        return OperationResult(transaction.transaction_id, self.__balance, f'{amount} успешно зачислены на счет.')
    
    def cancelation(self, amount: float, transaction_type: TransactionType) -> OperationResult:
        if amount <= 0:
            return OperationResult('', self.__balance, 'Нельзя использовать отрицательное значение.')
        msg = ''
        if transaction_type == TransactionType.DEPOSIT:
            self.__balance -= amount
            msg = '{amount} – были сняты со счета в счет отмены операции.'
        elif transaction_type == TransactionType.WITHDRAW:
            self.__balance += amount
            msg = '{amount} – были возвращены на счет из-за отмены операции.'
        transaction = self._add_transaction(TransactionType.CANCELATION, amount)
        return OperationResult(transaction.transaction_id, self.__balance, msg)

    def withdraw(self, amount: float) -> OperationResult:
        if amount <= 0:
            return OperationResult('', self.__balance, 'Нельзя снять отрицательное значение.')
        if self.__balance < amount:
            return OperationResult('', self.__balance, 'Нет средств для проведения операции.')
        self.__balance -= amount
        transaction = self._add_transaction(TransactionType.WITHDRAW, amount)
        return OperationResult(transaction.transaction_id, self.__balance, f'{amount} успешно сняты со счета.')

    def _add_transaction(self, operation: TransactionType, amount: float) -> Transaction:
        new_transaction = Transaction(operation=operation, amount=amount, balance_after=self.__balance)
        self._transactions.append(new_transaction)
        return new_transaction

    def show_history(self, filter_by: TransactionType | None = None) -> str:
        '''
        filter_by: тип транзакции (DEPOSIT, WITHDRAW) или None для отображения всех операций.
        '''
        history = [f'История транзакций для {self.name}']
        if filter_by:
            filtered_transactions = [t for t in self._transactions if t.operation == filter_by]
        else:
            filtered_transactions = self._transactions

        if not filtered_transactions:
            return 'История транзакций пуста.'

        history.extend([str(transaction) for transaction in filtered_transactions])
        return '\n'.join(history)

    def summary(self) -> str:
        deposits = sum(t.amount for t in self._transactions if t.operation == TransactionType.DEPOSIT)
        withdrawals = sum(t.amount for t in self._transactions if t.operation == TransactionType.WITHDRAW)
        summary_lines = [
            f'Данные об аккаунте: {self.name}',
            f'Всего зачислено: {deposits}',
            f'Всего снято: {withdrawals}',
            f'Нынешний баланс: {self.__balance}'
        ]
        return '\n'.join(summary_lines)

    def get_balance(self) -> float:
        return self.__balance

    def set_balance(self, amount: float) -> str:
        return 'Нельзя изменить баланс без совершения операции.'

    def cancel_transaction(self, transaction_id: str) -> OperationResult:
        for transaction in self._transactions:
            if transaction.transaction_id == transaction_id:
                cancelation_transaction = self.cancelation(transaction.amount, transaction_type=transaction.operation)
                return OperationResult(transaction_id, self.__balance, f'Транзакция {transaction_id} была отменена.')
        return OperationResult('', self.__balance, 'Транзакция не найдена.')

acc = Account('Роман Абрамович', 500)  # Создаем аккаунт с начальным балансом 500

result1 = acc.deposit(200)
print(result1)

result2 = acc.withdraw(100)
print(result2)

print(acc.show_history())

print(acc.summary())

transaction_id = result2.transaction_id
print(f'\nОтмена транзакции: {transaction_id}')
cancel_result = acc.cancel_transaction(transaction_id)
print(cancel_result)

print('История после отмены транзакции:')
print(acc.show_history())
