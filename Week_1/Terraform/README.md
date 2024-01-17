# Intro To Terraform

## What is Terraform
Terraform is an infrastructure-as-code software tool created by HashiCorp. Users define and provide data center and on prem infrastructure using a declarative configuration language known as HashiCorp Configuration Language. 
HCL files can be versioned, reused and shared. You can use a consistent workflow to provision and manage all infrastructure thorughout its lifecycle.

### Why use Terraform?
* Simplify tracking infra
* Easier collaboration
* Reproducability
* Ensure resources are removed after end of life

### What it is not
* Does not manager and update code directly on infra
* Cannot change immutable resources
* Cannot manage infra outside of resources defined within Terraform


## Key Commands
* init - fetches required providers
* plan - explain what I'm about to do
* apply - apply the hcl (create infra)
* destroy - destroy infra defined in the hcl (and stored in cache)






