# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from back_end.entity import StateNode, Base
#
# class StateNodeDAO:
#     def __init__(self, db_url='postgresql://postgres:postgres@localhost:5432/dama'):
#         self.engine = create_engine(db_url)
#         Base.metadata.create_all(self.engine)
#         self.Session = sessionmaker(bind=self.engine)
#
#     def create_node(self, node_data):
#         session = self.Session()
#         try:
#             node = StateNode(**node_data)
#             session.add(node)
#             session.commit()
#             return node.id
#         except Exception as e:
#             session.rollback()
#             print(f"Error creating node: {e}")
#         finally:
#             session.close()
#
#     def get_node(self, node_id):
#         session = self.Session()
#         try:
#             return session.query(StateNode).filter(StateNode.id == node_id).first()
#         finally:
#             session.close()
#
#     def update_node(self, node_id, updated_data):
#         session = self.Session()
#         try:
#             node = session.query(StateNode).filter(StateNode.id == node_id).first()
#             if node:
#                 for key, value in updated_data.items():
#                     setattr(node, key, value)
#                 session.commit()
#                 return True
#             return False
#         except Exception as e:
#             session.rollback()
#             print(f"Error updating node: {e}")
#         finally:
#             session.close()
#
#     def delete_node(self, node_id):
#         session = self.Session()
#         try:
#             node = session.query(StateNode).filter(StateNode.id == node_id).first()
#             if node:
#                 session.delete(node)
#                 session.commit()
#                 return True
#             return False
#         except Exception as e:
#             session.rollback()
#             print(f"Error deleting node: {e}")
#         finally:
#             session.close()
#
#     def get_all_nodes(self):
#         session = self.Session()
#         try:
#             return session.query(StateNode).all()
#         finally:
#             session.close()
