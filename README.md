# Telemetry As Code Demo

Demonstrate using Kibana SavedObjects + Terraform to show a simple Telemetry as Code example.

# Requirements

- Docker-Compose (usually installed with docker)
- Terraform
- My Terraform Elastic Provider - https://github.com/ansoni/terraform-provider-elastic

# Usage

	docker-compose up -d

This will start two pairs of kibana/elasticsearch on port 9200/5601 / 9400:5701 both on 127.0.0.1

Load the works of shakespheare into both.

	bash load_data.sh

Now Connect to the first kibana instance by visiting http://127.0.0.1:5701

Create an index Pattern/Save a Search/Create a visualization

Now export the data.

	python save.py

You will now have several files that are exported.

Now we can create a new terraform file to get things going:

	cat > test.tf << 'EOF'
	provider "elastic" {
	  url = "http://127.0.0.1:5601"
	}
	
	resource "elastic_kibana_index_pattern" "test" {
	  body = "${file("./out/index-pattern0.json")}"
	}
	
	resource "elastic_kibana_saved_search" "test" {
	  title = "test"
	  index_id = "${elastic_kibana_index_pattern.test.id}"
	  body = "${file("./out/search0.json")}"
	}
	EOF

We use an external provider for the demo.  It would be expected that we would use a module or even a custom provider if we went further and productized this.

Now apply the terraform

	terraform apply

Your index and saved_search should appear on the second kibana (http://127.0.0.1:5601

