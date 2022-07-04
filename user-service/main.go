package main

import (
	"fmt"
	"log"
	"net"
	"user-service/Configs"
	"user-service/Models"
	"user-service/Routes"
	server "user-service/Rpc/Server"

	"github.com/jinzhu/gorm"
	"google.golang.org/grpc"
)

func main() {
	var err error
	Configs.DB, err = gorm.Open("mysql", Configs.DbURL(Configs.BuildDBConfig()))
	if err != nil {
		fmt.Println("Status: ", err)
	}

	defer Configs.DB.Close()
	Configs.DB.AutoMigrate(
		&Models.User{},
		&Models.Administrator{},
	)
	Configs.DB.LogMode(true)

	s := server.Server{}

	grpcServer := grpc.NewServer()

	go serveGrpc(*grpcServer, s)

	r := Routes.SetupRouter()

	r.Run(":5001")
}

func serveGrpc(grpcServer grpc.Server, s server.Server) {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 6001))

	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	server.RegisterUserServiceServer(&grpcServer, &s)

	fmt.Println("USER-SERVICE GRPC: listening on 6001")

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %s", err)
	}
}
