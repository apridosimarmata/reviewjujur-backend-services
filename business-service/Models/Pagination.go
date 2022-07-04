package Models

type BusinessPagination struct {
	Limit       int         `json:"limit,omitempty;query:limit"`
	Page        int         `json:"page,omitempty;query:page"`
	Sort        string      `json:"sort,omitempty;query:sort"`
	LocationUid string      `json:"locationUid"`
	Location    string      `json:"location"`
	Province    string      `json:"province"`
	Query       string      `json:"query,omitempty"`
	TotalRows   int64       `json:"totalRows"`
	TotalPages  int         `json:"totalPages"`
	Rows        interface{} `json:"rows"`
}

func NewBusinessPagination() BusinessPagination {
	var BusinessPagination BusinessPagination
	BusinessPagination.Limit = 10
	BusinessPagination.Page = 1

	return BusinessPagination
}

func (p *BusinessPagination) GetOffset() int {
	return (p.GetPage() - 1) * p.GetLimit()
}

func (p *BusinessPagination) GetLimit() int {
	if p.Limit == 0 {
		p.Limit = 10
	}
	return p.Limit
}

func (p *BusinessPagination) GetPage() int {
	if p.Page == 0 {
		p.Page = 1
	}
	return p.Page
}

func (p *BusinessPagination) GetSort() string {
	if p.Sort == "" {
		p.Sort = "uid"
	}
	return p.Sort + " desc"
}
