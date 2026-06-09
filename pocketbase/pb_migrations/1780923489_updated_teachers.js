/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("fool5kx8yluzk2q")

  collection.createRule = "1=1"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("fool5kx8yluzk2q")

  collection.createRule = "@request.auth.id != \"\""

  return dao.saveCollection(collection)
})
