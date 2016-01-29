db.phh_record.aggregate(

  // Pipeline
  [
    // Stage 1
    {
      $unwind: "$data"
    },

    // Stage 2
    {
      $match: { "create_time": { $gte: ISODate("2016-01-06T16:00:00"), $lt: ISODate("2016-01-07T16:00:00") } }
    },

    // Stage 3
    {
      $project: {"district": "$data.district_name", "addr": "$data.shipping_address", "lng":"$data.lng","lat":"$data.lat", "node_name": "$data.node.name", "node_id": "$data.node.id", "tn": "$data.tracking_number", "_id": 0}
    },

    // Stage 4
    {
      $match: {
      node_name: "口口"
      }
    }

  ]

  // Created with 3T MongoChef, the GUI for MongoDB - http://3t.io/mongochef

);
