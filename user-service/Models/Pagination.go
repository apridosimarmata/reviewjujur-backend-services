package Models

type UserPagination struct {
	Limit      int         `json:"limit,omitempty;query:limit"`
	Page       int         `json:"page,omitempty;query:page"`
	Sort       string      `json:"sort,omitempty;query:sort"`
	Query      string      `json:"query,omitempty;query:query"`
	TotalRows  int64       `json:"totalRows"`
	TotalPages int         `json:"totalPages"`
	Rows       interface{} `json:"rows"`
}

func NewUserPagination() UserPagination {
	var userPagination UserPagination
	userPagination.Limit = 10
	userPagination.Page = 1

	return userPagination
}

func (p *UserPagination) GetOffset() int {
	return (p.GetPage() - 1) * p.GetLimit()
}

func (p *UserPagination) GetLimit() int {
	if p.Limit == 0 {
		p.Limit = 10
	}
	return p.Limit
}

func (p *UserPagination) GetPage() int {
	if p.Page == 0 {
		p.Page = 1
	}
	return p.Page
}

func (p *UserPagination) GetSort() string {
	if p.Sort == "" {
		p.Sort = "name"
	}
	return p.Sort + " desc"
}
