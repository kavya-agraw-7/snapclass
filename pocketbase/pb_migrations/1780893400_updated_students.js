/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  collection.listRule = "1=1"
  collection.viewRule = "1=1"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  collection.listRule = null
  collection.viewRule = null

  return dao.saveCollection(collection)
})
