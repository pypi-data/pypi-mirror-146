# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..base import Base


class Workflows(Base):

    """Used to sync workflows from a source instance to a destination instance of Swimlane
    """

    def sync_workflow(self, application_name: str):
        """This methods syncs a single applications workflow from a source Swimlane instance to 
        a destination instance.

        If an application_name is in our include or exclude filters we will either ignore or
        process the workflow updates for that application.

        Once an application_name is provided we retrieve the workflow for that application from 
        our workflow_dict. Additionally we retrieve the destination workflow for the provided
        application.

        We create a temporary object that compares the stages of a source workflow to a destination
        workflow. If they are exactly the same we skip updating the workflow. If they are not, we 
        copy the source workflow to the destination and update it to reflect the new workflow ID.

        Finally we update the destination workflow with our changes.

        Args:
            application_name (str): The name of an application to check and update workflow if applicable.
        """
        workflow = self.source_instance.workflow_dict.get(application_name)
        if workflow:
            self.__logger.info(f"Processing workflow '{workflow['id']}' for application '{application_name}' ({workflow['applicationId']}).")
            self.__logger.info(f"Adding workflow for application '{application_name}' ({self.source_instance.application_dict[application_name]['id']}).")
            dest_workflow = self.destination_instance.add_workflow(workflow=workflow)
            if not dest_workflow:
                dest_workflow = self.destination_instance.get_workflow(application_id=workflow['applicationId'])
                if workflow['stages'] != dest_workflow['stages']:
                    self.__logger.info(f"Updating workflow for application '{application_name}' ({self.source_instance.application_dict[application_name]['id']}).")
                    resp = self.destination_instance.update_workflow(workflow=workflow)
                    self.__logger.info(f"Successfully updated workflow for application '{application_name}'.")
                else:
                    self.__logger.info(f"No differences found in workflow. Skipping....")
            else:
                self.__logger.info(f"Successfully added workflow for application '{application_name}'.")

    def sync(self):
        """This method is used to sync all workflows from a source instance to a destination instance
        """
        raise NotImplementedError("General workflow syncing is currently not implemented.")
