class UnknownTransaction():
  def __init__(self, chain:str, address:str,
    transaction_id:str, reason:str):
    self.chain = chain
    self.address = address
    self.transaction_id = transaction_id
    self.reason = reason