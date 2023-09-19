1. What challenges do you see in these requirements?

      1. JSON with undefined fields will lead to confussion and is generally means we don't have a grasp of the needs of the system. Better to well define the fields we know and extend as we learn. Files - need more definition on what types of files we will be recieving - if these are industry standard types or if there are a few to start with we can better prioritize the development of any needed parsers.
      2. Fairly clear, but my assumption is that we all know what personal data we mean - its better to define where our line is. Names, Numbers, etc are clear but when it comes to things that allow fingerprinting like installed apps, is that something we should clean out?
      3. Clear - once we lock down file types its just a design consideration for how we asych process logs at that size. For a mobile device we should consider the battery impacts of shipping 500MB (daily?)
      4. Assumes we know which "fields and values" we expect in JSON - so that needs to get more locked down along with files and what data model we expect to overlap (assuming that the goal is to search them together). Also would want to know the access paterns that are planned - is this something that is done offline by the iVerify team (not a user), access controls and performance can be designed to match the needed paterns. This also likely leads us to storing more than one copy of the data - cost decisions should be made if we need this hot or cold.
      5. Data security will need to be planned out as well as data storage as things like GDPR and China's data sovernty laws will dictate where "customers data" needs to be and how it needs to be labeled.
      6. Assuming you mean the one we design and build - maybe not the most cost effective to rebuild something like that unless we have determined that we have some distinct vision that differs from all of the other platforms. May make more sense to build integration into common tools (via the HTTP endpoints).
      7. Assuming the same as the analytics platform (though very likely different datasets) - integration through API would be pretty standard. Would just need more information on what the SIEM expects as input. 

1. Design the infrastructure and describe it as detailed as you can. For instance, how the data storage will be organized? How many servers does it require? What restrictions and specifications will they have?
   1. Diagram is included with a handful of assumptions. We would need to better understand the legal requirements for data storage (must it remain in region/country?) for each of the customers, but storing data by customer into separate indexes provides isolation. The analytics datastore may WANT to have the data aggregated for better analysis and could be good to have some of the personal data as some emergent features in models are non-obvious. That said, likely best to remain clean and not introduce potental bias and regulatory/legal risk.

2. Describe communication between architecture components.
   1. Internally - all communication is done via AWS backbone (network level) and via AWS APIs (application level) using security roles with least-privledge. External communication (leaving AWS) would be done via API that is secured by an OAuth provider (I just put Auth0 as an example). That would allow us to scope each client and provide unique secrets to them for their access. This also allows us to cut access easily and rotate secrets.

3. Briefly describe measures to secure the communication channel, storage, and infrastructure at all.
   1. All data storage (bar S3 - not network) would be in private subnets - these are completely unroutable via the public internet. This shrinks the attack surface GREATLY and allows a reduced footprint to monitor for intrusion. APIs, are again secured by Oauth. The AWS IAM roles will secure inter-system communication.

4. Answer the following questions for the whole infrastructure:

   1. What challenges do you see? 
      1. Cost, storing data across multiple analytics clusters could get pricey (though serverless Redshift is MORE cost effective for these smaller use cases). Latency, not something I would expect, but something we should monitor.

   2. What solutions do you propose? 
      1. Deploy our API's (via ECS Fargate) into all of the general regions we plan to serve. Consider using single Redshift if we can legal do that.

   3. What cons and pros do the solutions have?
      1. Triple storing data isn't perfect by any stretch - but data storage method should map to data usage pattern, so not much to do about it unless we reduce functionality or accept performance/capability limitations. Single API for all customers could be limiting if customers have super specific needs but we could extend or build custom where needed.

_Be ready to answer for each requirement during the interview._