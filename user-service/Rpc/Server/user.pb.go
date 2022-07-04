// Code generated by protoc-gen-go. DO NOT EDIT.
// source: Rpc/Server/user.proto

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
	UnsuspendAt          int32    `protobuf:"varint,5,opt,name=unsuspendAt,proto3" json:"unsuspendAt,omitempty"`
	Uid                  string   `protobuf:"bytes,6,opt,name=uid,proto3" json:"uid,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *User) Reset()         { *m = User{} }
func (m *User) String() string { return proto.CompactTextString(m) }
func (*User) ProtoMessage()    {}
func (*User) Descriptor() ([]byte, []int) {
	return fileDescriptor_user_b1cc1bfe8db59bd8, []int{0}
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

func (m *User) GetUnsuspendAt() int32 {
	if m != nil {
		return m.UnsuspendAt
	}
	return 0
}

func (m *User) GetUid() string {
	if m != nil {
		return m.Uid
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
	return fileDescriptor_user_b1cc1bfe8db59bd8, []int{1}
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
	return fileDescriptor_user_b1cc1bfe8db59bd8, []int{2}
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
	Metadata: "Rpc/Server/user.proto",
}

func init() { proto.RegisterFile("Rpc/Server/user.proto", fileDescriptor_user_b1cc1bfe8db59bd8) }

var fileDescriptor_user_b1cc1bfe8db59bd8 = []byte{
	// 233 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x5c, 0x90, 0xcd, 0x4a, 0x03, 0x31,
	0x14, 0x85, 0x8d, 0x9d, 0xa9, 0x7a, 0xeb, 0xa2, 0x5c, 0x54, 0x42, 0x17, 0x32, 0x0c, 0x2e, 0xba,
	0x6a, 0x41, 0x7d, 0x01, 0x15, 0x71, 0xe7, 0x22, 0xda, 0x07, 0x88, 0x33, 0x57, 0x0c, 0x9a, 0x1f,
	0xf3, 0xa3, 0xf4, 0x6d, 0x7c, 0x54, 0x49, 0x84, 0xe9, 0xe0, 0xee, 0xdc, 0xef, 0x9e, 0x1c, 0x72,
	0x0f, 0x9c, 0x0a, 0xd7, 0xad, 0x9f, 0xc8, 0x7f, 0x91, 0x5f, 0xa7, 0x40, 0x7e, 0xe5, 0xbc, 0x8d,
	0x16, 0xab, 0xac, 0xdb, 0x1f, 0x06, 0xd5, 0x26, 0x90, 0xc7, 0x05, 0x1c, 0xbe, 0x76, 0xfa, 0xd9,
	0xbe, 0x93, 0xe1, 0xac, 0x61, 0xcb, 0x23, 0x31, 0xcc, 0x88, 0x50, 0x19, 0xa9, 0x89, 0xef, 0x17,
	0x5e, 0x34, 0x9e, 0x03, 0x7c, 0xbf, 0xc9, 0x18, 0xa4, 0x73, 0x8f, 0x96, 0x4f, 0xca, 0x66, 0x44,
	0xf0, 0x04, 0x6a, 0xd2, 0x52, 0x7d, 0xf0, 0xaa, 0xac, 0xfe, 0x06, 0x6c, 0x60, 0x96, 0x4c, 0x48,
	0xc1, 0x91, 0xe9, 0x6f, 0x22, 0xaf, 0x1b, 0xb6, 0xac, 0xc5, 0x18, 0xe1, 0x1c, 0x26, 0x49, 0xf5,
	0x7c, 0x5a, 0x5e, 0x65, 0xd9, 0x5e, 0xc0, 0x3c, 0xff, 0xf0, 0x76, 0xbb, 0x51, 0xbd, 0xa0, 0xcf,
	0x44, 0x61, 0x70, 0xb1, 0x9d, 0xeb, 0x00, 0xea, 0x7b, 0xed, 0xe2, 0xf6, 0xf2, 0x0e, 0x66, 0xd9,
	0x9e, 0x0f, 0x56, 0x1d, 0xe1, 0x35, 0x1c, 0x3f, 0x50, 0x1c, 0x02, 0xf0, 0x6c, 0x55, 0x3a, 0xf8,
	0x9f, 0xb8, 0x80, 0x1d, 0x6f, 0xf7, 0x5e, 0xa6, 0xa5, 0xa3, 0xab, 0xdf, 0x00, 0x00, 0x00, 0xff,
	0xff, 0x98, 0x7a, 0x70, 0x4e, 0x3c, 0x01, 0x00, 0x00,
}
