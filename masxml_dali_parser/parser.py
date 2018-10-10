from lxml import etree

class DefaultElement(etree.ElementBase):
  def query(self, query):
    return self.xpath(query)

  def words(self):
    return self.query("//W")

  def sentences(self):
    return self.query("//layMarkable[@layType='s']")

  def paragraphs(self):
    return self.query("//layMarkable[@layType='p']")

  def sections(self):
    return self.query("//layMarkable[@layType='section']")

  def ner(self):
    return self.query("//nerMarkable")

  def markable_heads(self):
    return self.query("//nh")

  def markables(self):
    return self.query("//am")

class AddressedElementBase(DefaultElement):
  @property
  def lookup_table(self):
    W_lookup_table = {el.get("id"): idx for idx, el in enumerate(self.xpath("//W"))}
    return W_lookup_table

  @property
  def offsets(self):
    start_id, end_id = self.id_offsets
    lookup_table = self.lookup_table
    return (lookup_table.get(start_id), lookup_table.get(end_id))

  def relative_offsets(self, containing_element):
    container_start, _ = containing_element.offsets
    start, end = self.offsets 
    return (start-container_start, end-container_start)

  def is_inside(self, element):
    """
    check to see if this element (self) is inside another
    """
    inside_start, inside_end = self.offsets
    outside_start, outside_end = element.offsets
    return (inside_start >= outside_start and inside_end <= outside_end)

  def query(self, query):
    start, end = self.offsets
    return [el for el in self.xpath(query) if el.is_inside(self)]

class IDAddressedElement(AddressedElementBase):
  @property
  def id_offsets(self):
    return (self.get("id"), self.get("id"))

class SpanAddressedElement(AddressedElementBase):
  @property
  def id_offsets(self):
    span = self.get("span")
    return tuple(span.split(".."))

class HeadAddressedElement(AddressedElementBase):
  @property
  def id_offsets(self):
    head = self.get("head")
    return tuple(head.split(".."))

class StartEndAddressedElement(AddressedElementBase):
  @property
  def id_offsets(self):
    return (self.get("start"), self.get("end"))

class MASXMLDALI_Lookup(etree.CustomElementClassLookup):
  element_addressing_types = {'W': IDAddressedElement,
      'nerMarkable': StartEndAddressedElement,
      'nh': HeadAddressedElement,
      'am': SpanAddressedElement,
      'layMarkable': StartEndAddressedElement}

  def lookup(self, node_type, document, namespace, name):
    return self.element_addressing_types.get(name, DefaultElement)

def parse(xml_string):
  parser = etree.XMLParser()
  parser.set_element_class_lookup(MASXMLDALI_Lookup())
  return etree.fromstring(xml_string, parser)
