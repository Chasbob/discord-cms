import * as React from "react";
import {
  List,
  Datagrid,
  Edit,
  Create,
  SimpleForm,
  DateField,
  TextField,
  EditButton,
  TextInput,
  DateInput,
  useAuthenticated,
} from "react-admin";

export const GuildList = (props) => {
  useAuthenticated(); // redirects to login if not authenticated
  return (
    <List {...props}>
      <Datagrid>
        <TextField source="id" />
        <TextField source="name" />
      </Datagrid>
    </List>
  );
};

const GuildTitle = ({ record }) => {
  return <span>Guild {record ? `"${record.title}"` : ""}</span>;
};

export const GuildEdit = (props) => (
  <Edit title={<GuildTitle />} {...props}>
    <SimpleForm>
      <TextInput source="name" />
      <TextInput multiline source="content" />
      <TextInput disabled source="channel" />
    </SimpleForm>
  </Edit>
);

export const GuildCreate = (props) => (
  <Create title="Create a Guild" {...props}>
    <SimpleForm>
      <TextInput source="title" />
      <TextInput source="teaser" options={{ multiLine: true }} />
      <TextInput multiline source="body" />
      <TextInput label="Publication date" source="published_at" />
      <TextInput source="average_note" />
    </SimpleForm>
  </Create>
);
