from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from backend.users.models import User

from backend.clients.dals.clients_dals import ClientDAL
from backend.collections.dals.track_group_dal import TrackCollectionDAL
from backend.collections.dals.main_group_dal import CollectionGroupDAL
from backend.auth import errors
from backend.auth.permissions import Permissions
from ..mixins import MusicMixin




from backend.general_schemas import ClientWithTrackCollection
from backend.collections.schemas import (TrackCollectionCreate, TrackCollectionShow,
                                   GroupCollectionWithTrackCollectionCreate,
                                   TrackCollectionUpdateResponse,
                                   AppendTrackCollectionToClient)



class TrackGroupCollectionHandler(MusicMixin):
  def __init__(self, session: AsyncSession, current_user: User = None) -> None:
    self.session = session
    self.track_collection_dal = TrackCollectionDAL(self.session)
    self.current_user = current_user
    self.permission = (Permissions(current_user))
  
  
  async def check_track_collection_in_db(self, track_collection_id: int):
    track_collection = await self.track_collection_dal.get_track_collection_by_id(track_collection_id)
    return track_collection
  
  
  async def __create_track_collection(self, body: dict):
    track_collection_created = await self.track_collection_dal.create_track_collection(
      name=body.get('track_collection_name'),
      player_option=body.get('player_option')
    )
    return track_collection_created
  
  
  async def _create_track_and_group_collections(self, body: TrackCollectionCreate):
    async with self.session.begin():
      if self.permission.redactor_permission():
        group_collection_dal = CollectionGroupDAL(self.session)
        model_data = body.model_dump(exclude_none=True)
        if self.check_body(model_data):
          group_coollection_id = model_data.pop('group_coollection_id')
          group_collection = await group_collection_dal.get_collection_group_for_track_collection(
            group_coollection_id
          )
          if group_collection is None:
            return JSONResponse(content=f'Collection with id = {group_coollection_id} not found',
                                status_code=404)
          
          track_collection = await self.__create_track_collection(body=model_data)
          
          group_collection.track_collections.append(track_collection)
          await self.session.commit()
          
          track_collection_show = TrackCollectionShow(
            id=track_collection.id,
            name=track_collection.name,
            player_option=track_collection.player_option
          )
          return GroupCollectionWithTrackCollectionCreate(
            id=group_collection.id,
            group_name=group_collection.group_name,
            track_collection=track_collection_show
          )
        else:
          return errors.not_parameters
      else:
        return errors.access_denied_error
  
  
  
  async def _get_track_collections_without_trakcs(self):
    async with self.session.begin():
      if self.permission.redactor_permission():
        track_collections = await self.track_collection_dal.get_all_track_collections_redactor()
        return list(track_collections)
      elif self.permission.client_permission():
        track_collections = await self.track_collection_dal.get_all_track_collections_client(
          user_id=self.current_user.id
        )
        return list(track_collections)
      else:
        return errors.access_denied_error
  
  
  
  async def _get_track_collection_by_id_without_trakcs(self, track_collection_id: int):
    async with self.session.begin():
      if self.permission.redactor_permission():
        track_collection_by_id = await self.track_collection_dal.get_track_collection_by_id_redactor(track_collection_id=track_collection_id)
        return track_collection_by_id
      elif self.permission.client_permission():
        track_collection_by_id = await self.track_collection_dal.get_track_collection_by_id_client(
          track_collection_id=track_collection_id, user_id=self.current_user.id
        )
        return track_collection_by_id
      else:
        return errors.access_denied_error
  
  
  
  async def _get_track_collections_with_tracks(self):
    async with self.session.begin():
      if self.permission.redactor_permission():
        track_collections = await self.track_collection_dal.get_track_collections_with_tracks_redactor()
        return list(track_collections)
      elif self.permission.client_permission():
        track_collections = await self.track_collection_dal.get_track_collections_with_tracks_client(user_id=self.current_user.id)
        return list(track_collections)
      else:
        return errors.access_denied_error
  
  
  
  async def _get_track_collection_by_id_with_tracks(self, track_collection_id: int):
    async with self.session.begin():
      if self.permission.redactor_permission():
        track_collection = await self.track_collection_dal.get_track_collection_by_id_with_tracks_redactor(
          track_group_id=track_collection_id
        )
        return track_collection
      elif self.permission.client_permission():
        track_collection = await self.track_collection_dal.get_track_collection_by_id_with_tracks_client(
          user_id=self.current_user.id, track_collection_id=track_collection_id
        )
        return track_collection
      else:
        return errors.access_denied_error
  
  
  
  async def _update_track_collection(self, track_collection_id: int, body: TrackCollectionUpdateResponse):
    async with self.session.begin():
      body_data = body.model_dump(exclude_none=True)
      updated_track_collection = await self.track_collection_dal.update_track_collection(track_collection_id, **body_data)
      return updated_track_collection
  
  
  
  async def _delete_track_collection(self, track_collection_id: int):
    async with self.session.begin():
      has_client = await self.track_collection_dal.collection_has_client(track_collection_id=track_collection_id)
      if has_client:
        return JSONResponse(content=f'Track collection {track_collection_id} has a client', status_code=403)
      deleted_track_collection = await self.track_collection_dal.delete_track_collection(track_collection_id)
      return deleted_track_collection
  
  
  
  async def _append_track_collection_to_client(self, body: AppendTrackCollectionToClient):
    if self.permission.redactor_permission():
      async with self.session.begin():
        body_data = body.model_dump(exclude_none=True)
        if self.check_body(body_data):
          client_dal = ClientDAL(self.session)
          client = await client_dal.get_client_for_append(
            client_id=body_data['client_id']
          )
          
          if client is None:
            return errors.found_error_in_db(
              'Client', body_data['client_id']
            )
          track_collection = await self.track_collection_dal.get_track_collection_for_append_client(
            track_group_id=body_data['track_collection_id']
          )
          if track_collection is None:
            return errors.found_error_in_db(
              'Track collection', body_data['track_collection_id']
            )  
          
          client.track_collections.append(track_collection)
          await self.session.commit()
          track_collection_data = TrackCollectionShow(
            id=track_collection.id,
            name=track_collection.name,
            player_option=track_collection.player_option
          )
          return ClientWithTrackCollection(
            id=client.id,
            name=client.name,
            city=client.city,
            email=client.email,
            phone=client.phone,
            price=client.price,
            track_collection=track_collection_data
          )
        else:
          return errors.not_parameters
    else:
      return errors.access_denied_error
  
  
  
  async def _delete_track_collection_from_client(self, body: AppendTrackCollectionToClient):
    if self.permission.redactor_permission():
      async with self.session.begin():
        body_data = body.model_dump(exclude_none=True)
        if self.check_body(body_data):
          client_dal = ClientDAL(self.session)
          if client_dal.check_client_in_db(body_data['client_id']) and self.check_track_collection_in_db(body_data['track_collection_id']):
            client = await client_dal.get_client_for_append(
              client_id=body_data['client_id']
            )
            track_collection = await self.track_collection_dal.get_track_collection_for_append_client(
              track_group_id=body_data['track_collection_id']
            )
            client.track_collections.remove(track_collection)
            await self.session.commit()
            return JSONResponse(f'Tack collection with id {body_data["track_collection_id"]} deleted from Client {body_data["client_id"]}',
                          status_code=200)
          else:
            return errors.not_Found_error
        else:
          return errors.not_parameters
    else:
      return errors.access_denied_error



