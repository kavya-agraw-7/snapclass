/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  collection.createRule = "1=1"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  collection.createRule = "@request.auth.id != \"\""

  return dao.saveCollection(collection)
})
