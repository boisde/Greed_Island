db.express.aggregate(

  // Pipeline
  [
    // Stage 1
    {
      $unwind: "$trace"
    },

    // Stage 2
    {
      $match: {
                  "trace.status" : "FINISHED",
                	"trace.actual_time": {
                              $gte: ISODate("2016-01-06T16:0:0"),
                              $lt: ISODate("2016-01-07T16:0:0")
                          },
              "courier.name": { $regex: "^((?!测试).)*$"}
          }
    },

    // Stage 3
    {
      $project: {
        _id: 0,
        expr_num: 1,
        status: 1,
        create_time: 1,
        "finish_time": "$trace.actual_time",
        "name": "$courier.name",
        "id": "$courier.id"
      }
    }
  ]

  // Created with 3T MongoChef, the GUI for MongoDB - http://3t.io/mongochef

);
