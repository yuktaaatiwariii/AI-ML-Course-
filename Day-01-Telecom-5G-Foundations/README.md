# Day 1 — Telecom & 5G Foundations for AI

**Module:** Telecom & 5G Foundations for AI  
**Type:** Theory / domain foundation  
**Status:** Completed

## 1. Day 1 objective

The first day established the telecom domain before moving into data and machine learning.

The central idea was:

> **Domain before data. Data before models. Models before deployment.**

A telecom analyst should understand what a metric physically represents before trying to model it.

---

# 2. Anatomy of a mobile network

A mobile network can be understood through four major layers.

## 2.1 RAN — Radio Access Network

The RAN contains the radio-side infrastructure:

- Antennas
- Radios
- Basebands
- Cell sites

The RAN is responsible for coverage, capacity and the air interface.

### Data generated

- PM (Performance Management) counters
- Cell-level KPIs
- Alarms

---

## 2.2 Transport

Transport consists of the backhaul/fronthaul links that carry traffic between sites and the core.

Examples:

- Fibre
- Microwave links

### Important metrics

- Link utilisation
- Latency
- Availability
- Outages

---

## 2.3 Core network

The core handles functions such as:

- Authentication
- Session management
- Mobility
- Routing
- Internet connectivity
- Inter-operator connectivity

### Data generated

- Session records
- Signalling logs
- CDRs

---

## 2.4 OSS / BSS

**OSS — Operations Support Systems**

**BSS — Business Support Systems**

These systems support both network operations and business operations.

They produce data such as:

- Billing records
- CRM records
- Customer tickets
- Orders
- Provisioning information

---

# 3. Evolution from 2G to 5G

## 2G — GSM

Main focus:

- Voice
- SMS
- Circuit-switched communication

Call Detail Records (CDRs) originate from this ecosystem and remain important for analytics.

## 3G — UMTS

Introduced stronger mobile data capabilities.

Data usage became a measurable and billable quantity.

## 4G — LTE

Major shift toward all-IP broadband.

Important customer-visible KPIs became:

- Throughput
- Latency
- Data usage

Voice also moved toward data-based delivery through technologies such as VoLTE.

## 5G — New Radio

5G adds capabilities such as:

- Higher capacity
- Lower latency
- Massive device density
- Network slicing
- Edge computing
- IoT support

---

# 4. Frequency and wavelength

One of the most important physical concepts for telecom analytics is:

**Higher frequency → shorter wavelength**

**Lower frequency → longer wavelength**

This affects coverage and capacity.

## Low band — around 700–900 MHz

Characteristics:

- Longer reach
- Better wall penetration
- Useful for rural coverage and indoor coverage
- Lower capacity compared with higher bands

## Mid band — roughly 1800 MHz–3.5 GHz

This provides a compromise between:

- Coverage
- Capacity

It is particularly important for urban 4G/5G networks.

## High band / mmWave

Example:

- 26 GHz and above

Characteristics:

- Very high capacity
- Shorter range
- More easily blocked by obstacles
- Useful for hotspots and high-density environments

### Why this matters for data analytics

If one region has lower throughput, that does not automatically mean the equipment is faulty.

The cause may be:

- Spectrum allocation
- Coverage
- Cell density
- Congestion
- User distribution

A good analyst connects the observed number to its physical cause.

---

# 5. 5G service classes

## eMBB — Enhanced Mobile Broadband

Optimises for:

**High data rate**

Use cases:

- Video
- AR
- Fixed wireless access
- High-bandwidth applications

## URLLC — Ultra-Reliable Low-Latency Communications

Optimises for:

- Very low latency
- High reliability

Use cases:

- Robotics
- Industrial automation
- Remote control

## mMTC — Massive Machine-Type Communications

Optimises for:

**Large numbers of connected devices**

Use cases:

- IoT sensors
- Smart meters
- Trackers

---

# 6. 5G architectural concepts

## Service-based architecture

The 5G core is designed around network functions communicating through software/API-based interfaces.

This represents a stronger convergence between telecom and IT.

## Network slicing

One physical network can support multiple logical networks, each designed around different performance requirements.

For example:

```text
Physical 5G Network
       │
       ├── Slice A → High throughput
       ├── Slice B → Ultra-low latency
       └── Slice C → Massive IoT
```

## Edge computing

Processing is moved closer to the user/device.

The objective is to reduce latency and avoid sending every workload to a distant central location.

---

# 7. Telecom business model

A key relationship introduced on Day 1:

```text
Revenue = Subscribers × ARPU
```

Telecom operators generally have three major commercial levers:

1. Acquire subscribers
2. Retain subscribers
3. Grow ARPU

---

# 8. Important telecom KPIs

## ARPU — Average Revenue Per User

Conceptually:

```text
ARPU = Total Revenue / Average Subscribers
```

ARPU is a commercial KPI used to understand revenue generated per subscriber.

## Churn rate

Represents subscriber loss over a period.

Conceptually:

```text
Churn Rate =
Disconnections / Opening Subscriber Base
```

Churn is a major machine-learning target later in the course.

## Downtime

Measures service unavailability.

It connects network reliability with customer/business impact.

## CSAT

Customer Satisfaction Score.

The course material presents it as a 1–5 satisfaction measure.

CSAT is useful but must be interpreted carefully because it can be sparse and biased.

---

# 9. Telecom data sources

Important sources introduced:

| Source | Meaning | Example data |
|---|---|---|
| CDR | Call Detail Records | Calls / sessions |
| PM | Performance Management | Cell KPIs |
| FM | Fault Management | Alarms |
| TT | Trouble Tickets | Incidents |
| BIL | Billing | Charges / payments |
| CRM | Customer Management | Customer interactions |
| IoT | Device telemetry | Continuous device data |

For every source, an analyst should ask:

1. Who owns it?
2. What is its grain?
3. How late can it arrive?
4. Can it be trusted?

---

# 10. Data grain

A very important analytical concept.

The Day 1 example used KPI data with:

**one row = one region × one month**

It was NOT:

- one row per subscriber
- one row per cell

Knowing the grain prevents incorrect aggregations and misleading analysis.

---

# 11. Scale of telecom data

The course introduced the scale of real telecom systems:

- 50M+ CDRs/day in the example
- ~500 GB raw usage/counter data per day
- ~10K analyst/dashboard queries per hour at peak
- PM counters often reported at 15-minute granularity

This explains why simple:

```python
pd.read_csv("huge_file.csv")
```

is not always an appropriate production strategy.

---

# 12. Traceability: counter → KPI → business decision

One of the most valuable concepts from Day 1 was the ability to trace a business metric back to the physical network.

Example:

```text
Network element
      ↓
Raw counter
      ↓
KPI
      ↓
Business signal
      ↓
Business decision
```

Example from the course:

```text
4G cell
 ↓
RRC connection attempts/successes
 ↓
Accessibility KPI
 ↓
Complaints + CSAT + churn movement
 ↓
Capacity decision
```

This is the mindset expected from a telecom data analyst.

---

# 13. Main Day 1 takeaways

- Telecom data comes from many network and business systems.
- Network architecture determines what data is generated.
- Frequency affects coverage and capacity.
- 5G introduces eMBB, URLLC and mMTC service classes.
- Telecom analytics requires domain understanding.
- ARPU, churn, downtime and CSAT are important business/network KPIs.
- Data grain must be understood before analysis.
- Large telecom datasets require scalable processing.
- Every dashboard number should ideally be traceable back to its source.

## One-line summary

**Day 1 taught me how telecom networks generate the data that later becomes the input for analytics and machine-learning systems.**
