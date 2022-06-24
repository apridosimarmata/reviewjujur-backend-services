// Code generated by protoc-gen-go. DO NOT EDIT.
// source: user.proto

package user

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type User struct {
	FcmToken             string   `protobuf:"bytes,1,opt,name=fcmToken,proto3" json:"fcmToken,omitempty"`
	Name                 string   `protobuf:"bytes,2,opt,name=name,proto3" json:"name,omitempty"`
	WhatsappNo           string   `protobuf:"bytes,3,opt,name=whatsappNo,proto3" json:"whatsappNo,omitempty"`
	Email                string   `protobuf:"bytes,4,opt,name=email,proto3" json:"email,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *User) Reset()         { *m = User{} }
func (m *User) String() string { return proto.CompactTextString(m) }
func (*User) ProtoMessage()    {}
func (*User) Descriptor() ([]byte, []int) {
	return fileDescriptor_user_ab9a34171faa3f81, []int{0}
}
func (m *User) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_User.Unmarshal(m, b)
}
func (m *User) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_User.Marshal(b, m, deterministic)
}
func (dst *User) XXX_Merge(src proto.Message) {
	xxx_messageInfo_User.Merge(dst, src)
}
func (m *User) XXX_Size() int {
	return xxx_messageInfo_User.Size(m)
}
func (m *User) XXX_DiscardUnknown() {
	xxx_messageInfo_User.DiscardUnknown(m)
}

var xxx_messageInfo_User proto.InternalMessageInfo

func (m *User) GetFcmToken() string {
	if m != nil {
		return m.FcmToken
	}
	return ""
}

func (m *User) GetName() string {
	if m != nil {
		return m.Name
	}
	return ""
}

func (m *User) GetWhatsappNo() string {
	if m != nil {
		return m.WhatsappNo
	}
	return ""
}

func (m *User) GetEmail() string {
	if m != nil {
		return m.Email
	}
	return ""
}

type UserByUidRequest struct {
	Uid                  string   `protobuf:"bytes,1,opt,name=uid,proto3" json:"uid,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *UserByUidRequest) Reset()         { *m = UserByUidRequest{} }
func (m *UserByUidRequest) String() string { return proto.CompactTextString(m) }
func (*UserByUidRequest) ProtoMessage()    {}
func (*UserByUidRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_user_ab9a34171faa3f81, []int{1}
}
func (m *UserByUidRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_UserByUidRequest.Unmarshal(m, b)
}
func (m *UserByUidRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_UserByUidRequest.Marshal(b, m, deterministic)
}
func (dst *UserByUidRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_UserByUidRequest.Merge(dst, src)
}
func (m *UserByUidRequest) XXX_Size() int {
	return xxx_messageInfo_UserByUidRequest.Size(m)
}
func (m *UserByUidRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_UserByUidRequest.DiscardUnknown(m)
}

var xxx_messageInfo_UserByUidRequest proto.InternalMessageInfo

func (m *UserByUidRequest) GetUid() string {
	if m != nil {
		return m.Uid
	}
	return ""
}

type Empty struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Empty) Reset()         { *m = Empty{} }
func (m *Empty) String() string { return proto.CompactTextString(m) }
func (*Empty) ProtoMessage()    {}
func (*Empty) Descriptor() ([]byte, []int) {
	return fileDescriptor_user_ab9a34171faa3f81, []int{2}
}
func (m *Empty) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Empty.Unmarshal(m, b)
}
func (m *Empty) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Empty.Marshal(b, m, deterministic)
}
func (dst *Empty) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Empty.Merge(dst, src)
}
func (m *Empty) XXX_Size() int {
	return xxx_messageInfo_Empty.Size(m)
}
func (m *Empty) XXX_DiscardUnknown() {
	xxx_messageInfo_Empty.DiscardUnknown(m)
}

var xxx_messageInfo_Empty proto.InternalMessageInfo

func init() {
	proto.RegisterType((*User)(nil), "user.User")
	proto.RegisterType((*UserByUidRequest)(nil), "user.UserByUidRequest")
	proto.RegisterType((*Empty)(nil), "user.Empty")
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// UserServiceClient is the client API for UserService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type UserServiceClient interface {
	GetUserByUid(ctx context.Context, in *UserByUidRequest, opts ...grpc.CallOption) (*User, error)
}

type userServiceClient struct {
	cc *grpc.ClientConn
}

func NewUserServiceClient(cc *grpc.ClientConn) UserServiceClient {
	return &userServiceClient{cc}
}

func (c *userServiceClient) GetUserByUid(ctx context.Context, in *UserByUidRequest, opts ...grpc.CallOption) (*User, error) {
	out := new(User)
	err := c.cc.Invoke(ctx, "/user.UserService/GetUserByUid", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// UserServiceServer is the server API for UserService service.
type UserServiceServer interface {
	GetUserByUid(context.Context, *UserByUidRequest) (*User, error)
}

func RegisterUserServiceServer(s *grpc.Server, srv UserServiceServer) {
	s.RegisterService(&_UserService_serviceDesc, srv)
}

func _UserService_GetUserByUid_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(UserByUidRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(UserServiceServer).GetUserByUid(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/user.UserService/GetUserByUid",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(UserServiceServer).GetUserByUid(ctx, req.(*UserByUidRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var _UserService_serviceDesc = grpc.ServiceDesc{
	ServiceName: "user.UserService",
	HandlerType: (*UserServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GetUserByUid",
			Handler:    _UserService_GetUserByUid_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "user.proto",
}

func init() { proto.RegisterFile("user.proto", fileDescriptor_user_ab9a34171faa3f81) }

var fileDescriptor_user_ab9a34171faa3f81 = []byte{
	// 195 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xe2, 0xe2, 0x2a, 0x2d, 0x4e, 0x2d,
	0xd2, 0x2b, 0x28, 0xca, 0x2f, 0xc9, 0x17, 0x62, 0x01, 0xb1, 0x95, 0x72, 0xb8, 0x58, 0x42, 0x8b,
	0x53, 0x8b, 0x84, 0xa4, 0xb8, 0x38, 0xd2, 0x92, 0x73, 0x43, 0xf2, 0xb3, 0x53, 0xf3, 0x24, 0x18,
	0x15, 0x18, 0x35, 0x38, 0x83, 0xe0, 0x7c, 0x21, 0x21, 0x2e, 0x96, 0xbc, 0xc4, 0xdc, 0x54, 0x09,
	0x26, 0xb0, 0x38, 0x98, 0x2d, 0x24, 0xc7, 0xc5, 0x55, 0x9e, 0x91, 0x58, 0x52, 0x9c, 0x58, 0x50,
	0xe0, 0x97, 0x2f, 0xc1, 0x0c, 0x96, 0x41, 0x12, 0x11, 0x12, 0xe1, 0x62, 0x4d, 0xcd, 0x4d, 0xcc,
	0xcc, 0x91, 0x60, 0x01, 0x4b, 0x41, 0x38, 0x4a, 0x2a, 0x5c, 0x02, 0x20, 0xdb, 0x9c, 0x2a, 0x43,
	0x33, 0x53, 0x82, 0x52, 0x0b, 0x4b, 0x53, 0x8b, 0x4b, 0x84, 0x04, 0xb8, 0x98, 0x4b, 0x33, 0x53,
	0xa0, 0x96, 0x82, 0x98, 0x4a, 0xec, 0x5c, 0xac, 0xae, 0xb9, 0x05, 0x25, 0x95, 0x46, 0xce, 0x5c,
	0xdc, 0x20, 0xe5, 0xc1, 0xa9, 0x45, 0x65, 0x99, 0xc9, 0xa9, 0x42, 0x26, 0x5c, 0x3c, 0xee, 0xa9,
	0x25, 0x70, 0x03, 0x84, 0xc4, 0xf4, 0xc0, 0xde, 0x41, 0x37, 0x51, 0x8a, 0x0b, 0x21, 0xae, 0xc4,
	0x90, 0xc4, 0x06, 0xf6, 0xae, 0x31, 0x20, 0x00, 0x00, 0xff, 0xff, 0x4e, 0xe6, 0xea, 0xac, 0xfc,
	0x00, 0x00, 0x00,
}
