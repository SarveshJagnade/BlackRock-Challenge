BlackRock Hackathon – Self-Saving Retirement API
📌 Overview

This project implements a production-grade financial API system that enables automated retirement savings using an expense-based micro-investment strategy.

The system:

Processes up to 1,000,000 transactions

Applies complex temporal financial rules (q, p, k periods)

Computes compound investment returns

Calculates NPS tax benefits

Adjusts returns for inflation

Exposes RESTful APIs

Runs fully containerized via Docker

This solution emphasizes:

Financial correctness

Algorithmic efficiency

Temporal data modeling

Database optimization

Enterprise software engineering practices

🏗 Architecture
Client
   ↓
FastAPI (Port 5477)
   ↓
Service Layer (Business Rules Engine)
   ↓
PostgreSQL (Range indexed temporal queries)
   ↓
Optional: Redis (caching)
Why PostgreSQL?

ACID compliance for financial integrity

Native tsrange support for temporal queries

GiST indexing for efficient period matching

Strong performance for 1M+ rows

Mature ecosystem

⚙️ Business Logic Summary
1️⃣ Transaction Builder

Rounds each expense to the next multiple of 100

Calculates remanent = ceiling − amount

2️⃣ q Period Rules (Override)

If transaction falls within q range:

Replace remanent with fixed value

If multiple match:

Use period with latest start date

3️⃣ p Period Rules (Addition)

Add all matching extra amounts

Applies even if q rule applied

4️⃣ k Period Rules (Grouping)

Transactions can belong to multiple k periods

Each k period is calculated independently

5️⃣ Investment Returns
NPS

7.11% annual compounding

Tax deduction capped at:

10% of annual income

₹2,00,000

Tax rebate calculated using defined slabs

Tax benefit returned separately

Index Fund (NIFTY 50)

14.49% annual compounding

No tax restrictions

Inflation Adjustment

Real value calculated using:

Real Return = Future Value / (1 + inflation)^years
📂 Project Structure
blackrock-retirement/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── services/
│   │     ├── transaction_service.py
│   │     ├── temporal_service.py
│   │     ├── returns_service.py
│   │     ├── tax_service.py
│
├── test/
│   ├── test_transactions.py
│   ├── test_temporal_rules.py
│   ├── test_returns.py
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
🗄 Database Design
transactions

id

timestamp (indexed)

amount

ceiling

remanent

q_periods

period (tsrange, indexed using GiST)

fixed

p_periods

period (tsrange, indexed using GiST)

extra

k_periods

period (tsrange)

Indexes are created to ensure efficient O(log n) temporal queries.

🚀 API Endpoints
1️⃣ Parse Transactions
POST /blackrock/challenge/v1/transactions:parse

Returns transactions enriched with ceiling and remanent.

2️⃣ Transaction Validator
POST /blackrock/challenge/v1/transactions:validator

Validates transactions against wage and constraints.

3️⃣ Temporal Constraints Filter
POST /blackrock/challenge/v1/transactions:filter

Applies q, p, k rules and returns valid/invalid transactions.

4️⃣ NPS Returns
POST /blackrock/challenge/v1/returns:nps

Returns:

savingsByDates

profits

taxBenefit

inflation adjusted values

5️⃣ Index Fund Returns
POST /blackrock/challenge/v1/returns:index

Returns:

savingsByDates

inflation adjusted returns

6️⃣ Performance Metrics
GET /blackrock/challenge/v1/performance

Returns:

execution time

memory usage

thread count

📊 Performance Considerations

Bulk insert operations

Indexed timestamp queries

GiST range indexing

SQL-based aggregation (avoiding Python loops)

Designed to scale to 10⁶ records

Time Complexity:

Transaction processing: O(n log n)

Period matching: O(log n) using range index

Group aggregation: Optimized SQL joins

🐳 Docker Deployment
Build Image
docker build -t blk-hacking-ind-sarvesh-jagnade .
Run Container
docker run -d -p 5477:5477 blk-hacking-ind-sarvesh-jagnade
 
 
Each test file contains:

Test type

Validation objective

Execution command

Run tests:

pytest

Testing includes:

Remanent calculation validation

q period override correctness

p period additive correctness

k grouping validation

Compound interest validation

Tax calculation correctness

📈 Financial Assumptions

Salary is pre-tax

Simplified tax slab model

No other deductions considered

Compounding applied annually

Inflation applied annually

If age ≥ 60, minimum 5 years considered

🔐 Data Integrity

Timestamp uniqueness enforced

Financial precision handled using NUMERIC types

ACID-compliant transactions

Strict validation layer

🌟 Beyond Requirements

This implementation also includes:

Clean layered architecture

Separation of financial logic from API layer

Performance monitoring endpoint

Dockerized environment

Scalable DB indexing strategy

Modular service architecture

Edge case handling

🧠 Design Philosophy

The system is designed to:

Minimize decision friction in savings

Provide mathematically correct financial projections

Ensure deterministic rule application

Scale to enterprise-grade transaction volumes

Maintain financial accuracy under temporal complexity

👨‍💻 Author

Sarvesh Dilip Jagnade
SDE – Backend / Full Stack Developer
FastAPI | PostgreSQL | Financial Systems | Distributed Architecture
