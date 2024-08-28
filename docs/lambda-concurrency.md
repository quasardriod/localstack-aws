# AWS Lamda

## Provisioned Concurrency
AWS Lambda's Provisioned Concurrency is a feature that enables you to prepare a specific number of execution environments to respond to requests instantly, with no cold starts. When a Lambda function is invoked, AWS normally allocates resources dynamically, which can lead to delays known as "cold starts." Provisioned Concurrency eliminates this delay by keeping a specified number of function instances warm and ready to handle requests.

### When and Why to Use Provisioned Concurrency
Provisioned Concurrency is particularly useful for:

High-traffic applications where low-latency response times are critical.
Predictable traffic patterns where you can anticipate spikes in usage.
Real-time data processing such as streaming applications where delays are unacceptable.

#### Provisioned Concurrency Testing
**Testing Strategies**
To ensure that your Lambda function behaves as expected under Provisioned Concurrency:

- ***Cold Start Tests:*** Measure the latency of the first request after setting up Provisioned Concurrency.
- ***Load Testing:*** Use tools like JMeter to simulate high traffic and measure the performance.
- ***Stress Testing:*** Gradually increase the load beyond normal levels to see how the function and Provisioned Concurrency handle extreme conditions.

#### Analyzing the Test Results
- ***Response Time:*** Should remain consistently low, indicating that Provisioned Concurrency is effectively reducing cold starts.
  - Observe metric of a Lambda Function with No Provisioned Concurrency and check difference.
- ***Throughput:*** Should increase linearly with the load until the provisioned concurrency limit is reached.
- ***Error Rate:*** Should be minimal; a high error rate might indicate that the function is hitting concurrency limits or other bottlenecks.

#### Key Metrics to Monitor
- ***ProvisionedConcurrentExecutions:*** Number of instances with Provisioned Concurrency enabled.
- ***ProvisionedConcurrencyUtilization:*** The percentage of provisioned instances that are currently in use.
- ***UnreservedConcurrentExecutions:*** Number of executions that are running without Provisioned Concurrency.
- ***Throttles:*** Number of times the function invocation was throttled.
  - When the number of concurrent executions exceeds the set limits, Lambda starts throttling new invocation requests. Throttled invocations receive a 429 error response (Too Many Requests), and event sources like Amazon S3 or Amazon SNS may retry the throttled requests, depending on their retry policies.
- ***Duration:*** The time your function takes to execute.